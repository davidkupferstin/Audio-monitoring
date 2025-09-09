import json

class UniqueIDGenerator:
    def __init__(self):
        pass

    def generates_id_from_metadata(self, metadata):
        size = metadata['size']
        last_modified = metadata['last_modified']

        unique_id = str(size) + last_modified.replace(" ", "")

        return unique_id






