from shared.logger.logger import Logger
import os
from services.classification.podcast_classification import PodcastClassification
from shared.elastic.connection import Connection
from shared.kafka.consumer import get_consumer


from dotenv import load_dotenv

load_dotenv()

class ClassificationService:
    def __init__(self):
        self.logger = Logger.get_logger()
        self.podcast_classification = PodcastClassification()
        Connection()
        self.es = Connection().es
        self.es_index = os.getenv("ES_INDEX")
        self.consumer = get_consumer('podcast_file_Transcript_to_es')


    def run(self):
            for record in self.consumer:
                id = record.value
                try:
                    response = self.es.get(index=self.es_index, id=id)
                    if response['found']:
                        document_source = response['_source']
                        if "field_name" in document_source:
                            file_transcript = document_source["field_name"]
                            classi_dict = self.podcast_classification.classification(file_transcript)
                        self.logger.info(f"Document found: {document_source}")
                    else:
                        self.logger.error(f"Document with ID '{id}' not found in index '{self.es_index}'.")
                except Exception as e:
                    self.logger.error(f"Error retrieving document: {e}")

                try:
                    response = self.es.update(index=self.es_index, id=id, body=classi_dict)
                    self.logger.info(f"File classification updated successfully: {response['result']}")
                except Exception as e:
                    self.logger.error(f"Error updating document: {e}")

                    # Optional: Verify the update by fetching the document
                # try:
                #     updated_doc = self.es.get(index=self.es_index, id=id)
                #     print(f"Updated document content: {updated_doc['_source']}")
                # except Exception as e:
                #     print(f"Error fetching document after update: {e}")

