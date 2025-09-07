from pathlib import Path
import datetime
import json

from extracting_files import ExtractingFiles

class ExtractingFileMetadata:
    def __init__(self):
        self.extracting_files = ExtractingFiles()

    def _convert_bytes_to_human_readable(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"


    def extract_metadata_to_json(self, path):
        file_path = Path(path)
        print(" \n")
        file_info = file_path.stat()

        absolute_path = path
        name = file_path.name
        size = file_info.st_size
        human_readable_size = self._convert_bytes_to_human_readable(file_info.st_size)
        creation_time = datetime.datetime.fromtimestamp(file_info.st_ctime)
        last_modified = datetime.datetime.fromtimestamp(file_info.st_mtime)

        data_string = {'path':
                        {'absolute_path': absolute_path},
                    'metadata' :
                        {'name': name,
                         'size': size,
                         'human_readable_size': human_readable_size,
                         'Creation_time': str(creation_time),
                         'last_modified': str(last_modified)}
                    }


        data_json = json.dumps(data_string, indent=4)
        return data_json


