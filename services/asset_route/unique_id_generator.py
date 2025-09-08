import json

class UniqueIDGenerator:
    def __init__(self):
        pass

    def generates_id_from_metadata(self, meta_record):
        data = json.loads(meta_record)
        size = data['metadata']['size']
        last_modified = data['metadata']['last_modified']

        unique_id = str(size) + last_modified.replace(" ", "")

        return unique_id






