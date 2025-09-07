from pathlib import Path
import datetime
from extracting_files import ExtractingFiles

def _convert_bytes_to_human_readable(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"



for path in ExtractingFiles().generates_file_paths():
    metadata = []
    file_path = Path(path)
    print(file_path)
    file_info = file_path.stat()

    absolute_path = {'absolute_path' : file_path}

    name = {'name' : file_path.name}

    size = {'size' : file_info.st_size}

    human_readable_size = {'human_readable_size' : _convert_bytes_to_human_readable(file_info.st_size)}

    creation_time = {'Creation_time' : datetime.datetime.fromtimestamp(file_info.st_ctime)}

    last_modified = {'last_modified' : datetime.datetime.fromtimestamp(file_info.st_mtime)}





    print(metadata)

