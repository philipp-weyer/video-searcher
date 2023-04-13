from flask_cors import CORS
from flask import Flask, request, send_from_directory
import flask
import os
import pymongo
import random
import uuid
from werkzeug.utils import secure_filename

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
app.config['UPLOAD_FOLDER'] = 'videos'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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

    if video:
        original_filename = secure_filename(video.filename)
        filename = str(uuid.uuid4()) + '.mp4'
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        response = flask.jsonify({
            'message': 'Upload successful'
        })
        return response

    response = flask.make_response(flask.jsonify({
        'message': 'Something went wrong'
    }), 400)
    return response
