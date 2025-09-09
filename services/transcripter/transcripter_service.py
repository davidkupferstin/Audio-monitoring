import os
import time
from services.transcripter.audio_transcript import AudioTranscript
from services.transcripter.mongo_manager import MongoManager
from shared.db.connector import MongoDBConnection
from shared.kafka.consumer import get_consumer


from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


class TranscripterService:
    def __init__(self):
        self.trans = AudioTranscript()
        self.consumer = get_consumer('podcast_file_to_mongo_id')

    def processes(self):
        pass



    def run(self):
        if not MONGO_URI or not DB_NAME:
            return "Missing MONGO_URI or DB_NAME in environment."
        # שליפת שם ןתוכן
        with MongoDBConnection(MONGO_URI, DB_NAME) as mongo_conn:
            manager = MongoManager(mongo_conn.db, COLLECTION_NAME)
            # while True:
            #     batch = manager.fetch_next(limit=100)
            #     if not batch:
            #         print("No more files to retrieve. Waiting for new data....")
            #         time.sleep(60)
            #         continue
            #     for file_record in batch:
            #         file = file_record['file']
            #         trans_file = self.trans.audio_content_to_readable_transcription(file)
            #         print(trans_file)
            #         # דחיפה לindex חדש בes
            #         #קובץ נוסף נדחף
            #     time.sleep(60)
            for record in self.consumer:
                file_record = manager.document(record.value)
                print(file_record)
                file = file_record
                trans_file = self.trans.audio_content_to_readable_transcription(file)
                print(trans_file)


