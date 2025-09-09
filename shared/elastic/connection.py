import pandas as pd
from elasticsearch import Elasticsearch, helpers
import time
import os

from dotenv import load_dotenv

load_dotenv()



class Connection:
    def __init__(self):
        elastic_uri = os.getenv("ELASTIC_URI")
        self.es = Elasticsearch("http://localhost:9200")
        while True:
            a = self.es.ping()
            if a:
                # print("Elasticsearch connection successful!")
                break
            # print("Could not connect to Elasticsearch.")
            time.sleep(5)


class Index:
    def __init__(self, index_name, index_mapping):
        self.es = Connection().es
        self.index_name = index_name
        self.index_mapping = index_mapping
        self.true_index = self.index_check_creation()

    def index_check_creation(self):
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)

        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)
            # self.es.indices.put_mapping(index=self.index_name, body=self.index_mapping)
        return self.es.indices.exists(index=self.index_name)

# class DocumentsIndex:
#     def __init__(self, index_name, index_mapping=None , ):
#         self.es = Connection().es
#         # if index_mapping is None:
#         #     index_mapping = {
#         #         'properties': {
#         #         }
#         #     }
#         self.index_name = index_name
#         self.index_mapping = index_mapping
#         Index(self.index_name, self.index_mapping)
#         self.indexes_documents()
#
#
#
#     def indexes_documents(self, documents):
#         try:
#             success, failed = helpers.bulk(self.es, documents)
#             # print(f"Successfully indexed {success} documents, {failed} failed.")
#
#             self.es.indices.refresh(index=self.index_name)
#         except Exception as e:
#             print(f"An error: {e}")
#


# class Retrieval:
#     def __init__(self, index_name, es, query=None, size=1000):
#         if query is None:
#             query = {
#                 "query": {"match_all": {}}
#             }
#         self.index_name = index_name
#         self.es = es
#         self.query = query
#         self.size = size
#
#     def get_retrieval(self):
#         return helpers.scan(
#             self.es,
#             index=self.index_name,
#             query=self.query,
#             size=self.size
#         )
#
#
# def print_results(results):
#     print(f"Found {results['hits']['total']['value']} results.")
#     for hit in results['hits']['hits']:
#         print(hit)
#         # print(f"ID: {hit['_id']}")
#         # print(f"Text: {hit['_source']['text'][:200]}...\n")  # Print first 200 characters
#
#
# class Main:
#     client = Connection()
#     index = DocumentsIndex()
#     es = client.es
#     index_name = index.index_name
#
#     query = {
#         "query": {"match_all": {}}
#     }
#
#     results = es.search(index=index_name, body=query)
#
#     print(f"Found {results['hits']['total']['value']} results.")
#     for hit in results['hits']['hits']:
#         # pprint(hit)
#         print(f"TweetID: {hit['_source']['TweetID']}\n")
#         print(f"CreateDate: {hit['_source']['CreateDate']}\n")
#         print(f"Antisemitic: {hit['_source']['Antisemitic']}\n")
#         print(f"Text: {hit['_source']['text'][:20]}...\n")  # Print first 20 characters
#         print(f"sentiment: {hit['_source']['sentiment']}\n")
#         print(f"weapons: {hit['_source']['weapons']}\n")
#
#
# Main()
#
# # for i in range(len(tweets_injected)):
# #     try:
# #         response = es.get(index=index_name, id=i)
# #         if response["found"]:
# #             print(f"Document found: {response['_source']}")
# #         else:
# #             print(f"Document with ID '{i}' not found in index '{index_name}'.")
# #     except Exception as e:
# #         print(f"Error retrieving document: {e}")
#
# # results = es.search(index=index_name, body=query)
# #
# #
