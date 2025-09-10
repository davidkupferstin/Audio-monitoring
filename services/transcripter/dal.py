class MongoDAL:
    def __init__(self, db = None):
        self.db = db

    def fetch_next_batch(self, collection_name, skip=0, limit=100):
        collection = self.db[collection_name]
        cursor = collection.find({}).sort([("createdate", 1), ("_id", 1)]).skip(skip).limit(limit)
        return list(cursor)

    def fetch_document(self, collection_name , value):
        collection = self.db[collection_name]
        result = collection.find_one({"unique_id": value}, {"file": 1 })
        return result

