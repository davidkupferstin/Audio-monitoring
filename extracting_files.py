import os
from dotenv import load_dotenv

load_dotenv()

class ExtractingFiles:
    def __init__(self):
        self.folder_path = os.getenv("FOLDER_PATH")

    def generates_file_paths(self):
        file_names = [f for f in os.listdir(self.folder_path)]

        for file_name in file_names:
            full_path = os.path.join(self.folder_path, file_name)
            yield full_path

