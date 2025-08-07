from db.mongo_client import get_mongo_collection

collection = get_mongo_collection()

def find_transcript(video_id: str):
    return collection.find_one({"video_id": video_id})

def save_transcript(transcript_data: dict):
    collection.insert_one(transcript_data)
