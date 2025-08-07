from pymongo import MongoClient

def get_mongo_collection():
    client = MongoClient("mongodb://yt-transcript-api-mongo-1:27017/")
    db = client.transcript_db
    return db.transcripts
