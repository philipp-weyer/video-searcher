from flask_cors import CORS
from flask import Flask, request, send_from_directory
import flask
import os
import pymongo
import random
import uuid
from werkzeug.utils import secure_filename

import thumbnail

from config import MONGO_URL, MONGO_DB

#  client = pymongo.MongoClient(MONGO_URL)
#  database = client.get_database(MONGO_DB)

def getTestVideo():
    testVideo = {
        'img': 'mongodb_logo.png',
        '_id': random.randint(0, 1000000),
        'title': 'This is an example title'
    }

    return testVideo

app = Flask(__name__)
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
    videos = [
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo(),
        getTestVideo()
    ]

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

    response = flask.make_response(flask.jsonify({
        'message': 'Upload successful'
    }))
    return response
