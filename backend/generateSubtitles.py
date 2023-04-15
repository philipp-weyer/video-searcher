import pymongo
import sys
import whisper

from config import MONGO_URL, MONGO_DB

def transcribe(video, db):
    videoPath = video['path']
    videoId = video['_id']

    model = whisper.load_model('base')

    print('Whisper model loaded')

    result = model.transcribe(videoPath)

    print('Transcription generated')

    segments = []

    for segment in result['segments']:
        segment['video_id'] = videoId
        segments.append(segment)

    print('Inserting segments')

    db.segments.insert_many(segments)

    print('Updating video')

    db.videos.update_one({'_id': videoId}, {
        '$set': {
            'text': result['text']
        }
    })

def watchVideoCollection(db):
    change_stream = db.videos.watch()

    for change in change_stream:
        if change['operationType'] == 'insert':
            print('Video was uploaded')
            transcribe(change['fullDocument'], db)

def subtitleService():
    while True:
        try:
            client = pymongo.MongoClient(MONGO_URL)
            database = client.get_database(MONGO_DB)

            watchVideoCollection(database)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass

if __name__ == '__main__':
    subtitleService()
