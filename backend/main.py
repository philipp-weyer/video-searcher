from bson import ObjectId
from flask_cors import CORS
from flask import Flask, request, send_from_directory
from flask.json import JSONEncoder
import flask
from multiprocessing import Process
import os
import pymongo
import random
import uuid
from werkzeug.utils import secure_filename

import thumbnail

from config import MONGO_URL, MONGO_DB, FRONTEND_PATH

from generateSubtitles import subtitleService

p = Process(target=subtitleService)
p.start()

client = pymongo.MongoClient(MONGO_URL)
database = client.get_database(MONGO_DB)

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super(CustomJSONEncoder, self).default(o)

def getTestVideo():
    testVideo = {
        'img': 'mongodb_logo.png',
        '_id': random.randint(0, 1000000),
        'title': 'This is an example title'
    }

    return testVideo

app = Flask(__name__, static_folder=FRONTEND_PATH)
app.json_encoder = CustomJSONEncoder
CORS(app)

app.config['VIDEO_FOLDER'] = 'videos'
if not os.path.exists(app.config['VIDEO_FOLDER']):
    os.makedirs(app.config['VIDEO_FOLDER'])

app.config['THUMBNAIL_FOLDER'] = 'thumbnails'
if not os.path.exists(app.config['THUMBNAIL_FOLDER']):
    os.makedirs(app.config['THUMBNAIL_FOLDER'])

@app.route("/", methods=["GET"], defaults={'path': ''})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/getVideos", methods=["GET"])
def getVideos():
    if 'text' not in request.args:
        videos = list(database.videos.find())
    else:
        videos = list(database.videos.aggregate([{
            '$search': {
                'compound': {
                    'should': [{
                        'text': {
                            'query': request.args['text'],
                            'path': 'title',
                            'fuzzy': {
                                'maxEdits': 2
                            }
                        }
                    }, {
                        'text': {
                            'query': request.args['text'],
                            'path': 'text',
                            'fuzzy': {
                                'maxEdits': 2
                            }
                        }
                    }]
                }
            }
        }, {
            '$project': {
                'text': 0
            }
        }]))

    response = flask.jsonify(videos)
    return response

@app.route("/videos/<path:path>")
def serveVideos(path):
    return send_from_directory('videos', path)

@app.route("/thumbnails/<path:path>")
def serveThumbnails(path):
    return send_from_directory('thumbnails', path)

def generateThumbnail(videoPath):
    options = {
        'trim': False,
        'height': 300,
        'width': 300,
        'quality': 85,
        'type': 'thumbnail'
    }

    thumbnailFilename = str(uuid.uuid4()) + '.jpg'
    thumbnailPath = os.path.join(app.config['THUMBNAIL_FOLDER'],
                                 thumbnailFilename)

    thumbnail.generate_thumbnail(videoPath, thumbnailPath, options)

    return thumbnailPath

@app.route("/uploadVideo", methods=['POST'])
def uploadVideo():
    if 'title' not in request.form:
        response = flask.make_response(flask.jsonify({
            'message': 'No title in request'
        }), 400)
        return response

    if 'video' not in request.files:
        response = flask.make_response(flask.jsonify({
            'message': 'No video in request'
        }), 400)
        return response

    video = request.files['video']

    if video.filename == '':
        response = flask.make_response(flask.jsonify({
            'message': 'No video selected'
        }), 400)
        return response

    original_filename = secure_filename(video.filename)
    filename = str(uuid.uuid4()) + '.mp4'
    path = os.path.join(app.config['VIDEO_FOLDER'], filename)
    video.save(path)

    thumbnailPath = generateThumbnail(path)

    database.videos.insert_one({
        'img': thumbnailPath,
        'title': request.form['title'],
        'path': path,
        'original_filename': original_filename
    })

    response = flask.make_response(flask.jsonify({
        'message': 'Upload successful'
    }))
    return response

@app.route("/getSegments/<video>", methods=["GET"])
def getSegments(video):
    aggregation = []

    if 'text' in request.args:
        aggregation += [{
            '$search': {
                'text': {
                    'query': request.args['text'],
                    'path': 'text',
                    'fuzzy': {
                        'maxEdits': 2
                    }
                },
                'highlight': {
                    'path': 'text'
                }
            }
        }, {
            '$set': {
                'highlights': {
                    '$meta': 'searchHighlights'
                }
            }
        }]

    aggregation += [{
        '$match': {
            'video_id': ObjectId(video)
        }
    }]

    if 'text' not in request.args:
        aggregation += [{
            '$sort': {
                'start': 1
            }
        }]

    videos = list(database.segments.aggregate(aggregation))

    response = flask.jsonify(videos)
    return response

@app.route('/deleteVideo/<videoId>')
def deleteVideo(videoId):
    video = database.videos.find_one({'_id': ObjectId(videoId)})

    database.segments.delete_many({'video_id': ObjectId(videoId)})
    database.videos.delete_one({'_id': ObjectId(videoId)})

    os.remove(video['path'])
    os.remove(video['img'])

    response = flask.jsonify({'message': 'Delete successful'})

    return response

@app.route('/getSubtitleStatus')
def getSubtitleStatus():
    missingSubtitles = database.videos.aggregate([{
        '$match': {
            'text': {
                '$exists': False
            }
        }
    }, {
        '$project': {
            'title': 1
        }
    }])

    response = flask.jsonify(list(missingSubtitles))

    return response
