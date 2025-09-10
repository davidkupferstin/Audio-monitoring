import os
from services.classification.podcast_classification import PodcastClassification
from shared.elastic.connection import Connection
from shared.kafka.consumer import get_consumer


from dotenv import load_dotenv

load_dotenv()

class ClassificationService:
    def __init__(self):
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
                        print(f"Document found: {document_source}")
                    else:
                        print(f"Document with ID '{id}' not found in index '{self.es_index}'.")
                except Exception as e:
                    print(f"Error retrieving document: {e}")

                try:
                    response = self.es.update(index=self.es_index, id=id, body=classi_dict)
                    print(f"Document updated successfully: {response}")
                except Exception as e:
                    print(f"Error updating document: {e}")

                    # Optional: Verify the update by fetching the document
                # try:
                #     updated_doc = self.es.get(index=self.es_index, id=id)
                #     print(f"Updated document content: {updated_doc['_source']}")
                # except Exception as e:
                #     print(f"Error fetching document after update: {e}")

