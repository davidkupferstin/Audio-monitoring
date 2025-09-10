from shared.logger.logger import Logger
import os
import  json
from services.asset_route.retrieving_files import RetrievingFiles
from services.asset_route.unique_id_generator import UniqueIDGenerator
from shared.kafka.consumer import get_consumer
from shared.db.connector import MongoDBConnection
from shared.elastic.connection import Connection, Index
from services.asset_route.dal import PersisterDAL
from shared.kafka.producer import send_messages


from dotenv import load_dotenv

load_dotenv()

class AssetRouteService:
    def __init__(self):
        self.logger = Logger.get_logger()
        self.unique_id_generator = UniqueIDGenerator()
        self.retrieving_files = RetrievingFiles()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME")
        Connection()
        self.es = Connection().es
        self.es_index = os.getenv("ES_INDEX")
        with open('index_mapping.json', 'r') as f:
            ES_INDEX_MAPPING = json.load(f)
        self.os_index_mapping = ES_INDEX_MAPPING
        Index(self.es_index, self.os_index_mapping)
        self.consumer = get_consumer('podcast_file_metadata')


    def preparing_the_data_parts(self, meta_record):
        id = self.unique_id_generator.generates_id_from_metadata(meta_record['metadata'])
        file = self.retrieving_files.content_in_binary_form(meta_record['path']['absolute_path'])
        metadata = meta_record['metadata']

        return id , file, metadata

    def mongo_persist(self, db, data):
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
                    id, file, metadata = self.preparing_the_data_parts(data)
                    data = {"unique_id" : id , "file" : file}
                    try:
                        self.mongo_persist(db, data)
                        send_messages('podcast_file_to_mongo_id', [id])
                        self.logger.info("The binary document was successfully written to Mongo.")
                    except Exception as e:
                        self.logger.error(f"Document not written: {e}")
                    document={"metadata" : metadata}
                    try:
                        response = self.es.index(index=self.es_index, id=id, document=document)
                        self.logger.info(f"File metadata indexed successfully: {response['result']}")
                    except Exception as e:
                        self.logger.error(f"Error indexing document: {e}")

                    # # Optional: Verify the document exists (search example)
                    # try:
                    #     search_response = self.es.get(index=self.es_index, id=id)
                    #     print("\nRetrieved document:")
                    #     print(search_response['_source'])
                    # except Exception as e:
                    #     print(f"Error retrieving document: {e}")

        except KeyboardInterrupt:
            self.logger.error("Shutting down AssetRouteService...")
        finally:
            self.consumer.close()