from shared.logger.logger import Logger
from services.meta_flow.extracting_files import ExtractingFiles
from services.meta_flow.extracting_file_metadata import ExtractingFileMetadata
from shared.kafka.producer import send_messages



class MetaFlowService:
    def __init__(self):
        self.extracting_files = ExtractingFiles()
        self.extracting_file_metadata = ExtractingFileMetadata()


    def file_metadata_record(self):
        for path in self.extracting_files.generates_file_paths():
            yield self.extracting_file_metadata.extract_metadata_to_json(path)



    def run(self):
        for record in self.file_metadata_record():
            send_messages('podcast_file_metadata', [record])

