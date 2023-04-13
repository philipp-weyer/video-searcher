from bson import ObjectId
from flask_cors import CORS
from flask import Flask, request, send_from_directory
from flask.json import JSONEncoder
import flask
import os
import pymongo
import random
import uuid
from werkzeug.utils import secure_filename
import whisper

import thumbnail

from config import MONGO_URL, MONGO_DB

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

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
CORS(app)

app.config['VIDEO_FOLDER'] = 'videos'
if not os.path.exists(app.config['VIDEO_FOLDER']):
    os.makedirs(app.config['VIDEO_FOLDER'])

app.config['THUMBNAIL_FOLDER'] = 'thumbnails'
if not os.path.exists(app.config['THUMBNAIL_FOLDER']):
    os.makedirs(app.config['THUMBNAIL_FOLDER'])

@app.route("/getVideos", methods=["GET"])
def getVideos():
    #  videosCollection = database.videos
    #  videos = videosCollection.findMany({})
    videos = list(database.videos.find())
    #  videos = [
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo(),
        #  getTestVideo()
    #  ]

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

def transcribe(videoPath, videoId):
    model = whisper.load_model('base')
    result = model.transcribe(videoPath)

    segments = []

    for segment in result['segments']:
        segment['video_id'] = videoId
        segments.append(segment)

    database.segments.insert_many(segments)

    database.videos.update_one({'_id': ObjectId(videoId)}, {
        '$set': {
            'text': result['text']
        }
    })

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

    result = database.videos.insert_one({
        'img': thumbnailPath,
        'title': request.form['title'],
        'path': path,
        'original_filename': original_filename
    })

    transcribe(path, result.inserted_id)

    response = flask.make_response(flask.jsonify({
        'message': 'Upload successful'
    }))
    return response

@app.route("/getSegments/<video>", methods=["GET"])
def getSegments(video):
    aggregation =[{
        '$match': {
            'video_id': ObjectId(video)
        }
    }, {
        '$sort': {
            'start': 1
        }
    }]

    if 'text' in request.args:
        search = {
            '$search': {
                'text': {
                    'query': request.args['text'],
                    'path': 'text',
                    'fuzzy': {
                        'maxEdits': 2
                    }
                }
            }
        }
        aggregation.insert(0, search)

    videos = list(database.segments.aggregate(aggregation))

    response = flask.jsonify(videos)
    return response
