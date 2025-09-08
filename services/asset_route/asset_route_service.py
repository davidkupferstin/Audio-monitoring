import os
import  json
from services.asset_route.retrieving_files import RetrievingFiles
from services.asset_route.unique_id_generator import UniqueIDGenerator
from shared.kafka.consumer import get_consumer
from shared.db.connector import MongoDBConnection
from shared.elastic.connection import Connection, DocumentsIndex
from services.asset_route.dal import PersisterDAL

from dotenv import load_dotenv

load_dotenv()

class AssetRouteService:
    def __init__(self):
        self.unique_id_generator = UniqueIDGenerator()
        self.retrieving_files = RetrievingFiles()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME")
        self.elastic_client = Connection()
        self.consumer = get_consumer('podcast_file_metadata')


    def preparing_the_data_parts(self, meta_record):
        id = self.unique_id_generator.generates_id_from_metadata(meta_record)
        file = self.retrieving_files.content_in_binary_form(meta_record)

        return id , file

    def persist(self, db, data):
        collection = db['podcast_files']
        if collection is not None:
            PersisterDAL.insert_document(collection, data)


    def run(self):
        try:
            with MongoDBConnection(self.mongo_uri, self.db_name) as mongo_conn:
                db = mongo_conn.db
                for record in self.consumer:
                    meta_record = record.value
                    data = json.loads(meta_record)
                    id, file = self.preparing_the_data_parts(data)
                    DocumentsIndex("podcast_file_metadata", id, data["metadata"])
                    data = {"_id" : id , "file" : file}
                    self.persist(db, data)



        except KeyboardInterrupt:
            print("Shutting down AssetRouteService...")
        finally:
            self.consumer.close()