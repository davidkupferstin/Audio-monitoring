import os
import time
from services.transcripter.audio_transcript import AudioTranscript
from services.transcripter.mongo_manager import MongoManager
from shared.db.connector import MongoDBConnection
from shared.elastic.connection import Connection, Index
from shared.kafka.consumer import get_consumer
from shared.kafka.producer import send_messages



from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


class TranscripterService:
    def __init__(self):
        self.transcript = AudioTranscript()
        Connection()
        self.es = Connection().es
        self.es_index = os.getenv("ES_INDEX")

        self.consumer = get_consumer('podcast_file_to_mongo_id')

    def processes(self):
        pass



    def run(self):
        if not MONGO_URI or not DB_NAME:
            return "Missing MONGO_URI or DB_NAME in environment."
        # שליפת שם ןתוכן
        try:
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
                #         trans_file = self.transcript.audio_content_to_readable_transcription(file)
                #         print(trans_file)
                #         # דחיפה לindex חדש בes
                #         #קובץ נוסף נדחף
                #     time.sleep(60)
                for record in self.consumer:
                    id = manager.document(record.value)
                    transcript_file = self.transcript.audio_content_to_readable_transcription(id)
                    update_body = {
                        "doc": {
                            "transcript_file": transcript_file
                        }
                    }
                    try:
                        response = self.es.update(index=self.es_index, id=id, body=update_body)
                        print(f"Document updated successfully: {response}")
                        send_messages('podcast_file_Transcript_to_es', [record.value])
                    except Exception as e:
                        print(f"Error updating document: {e}")

                    # # Optional: Verify the update by fetching the document
                    # try:
                    #     updated_doc = self.es.get(index=self.es_index, id=id)
                    #     print("\nUpdated Document Source:")
                    #     print(updated_doc["_source"])
                    # except Exception as e:
                    #     print(f"Error fetching updated document: {e}")
        except KeyboardInterrupt:
            print("Shutting down TranscripterService...")
        finally:
            self.consumer.close()
