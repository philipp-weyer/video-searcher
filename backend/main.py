from flask import Flask
import flask
import pymongo
import random

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
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
