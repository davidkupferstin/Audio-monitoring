import json

class UniqueIDGenerator:
    def __init__(self):
        pass

    def generates_id_from_metadata(self, meta_record):
        size = meta_record['metadata']['size']
        last_modified = meta_record['metadata']['last_modified']

        unique_id = str(size) + last_modified.replace(" ", "")

        return unique_id






