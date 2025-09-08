from services.asset_route.retrieving_files import RetrievingFiles
from services.asset_route.unique_id_generator import UniqueIDGenerator
from shared.kafka.consumer import get_consumer

class AssetRouteService:
    def __init__(self):
        self.unique_id_generator = UniqueIDGenerator()
        self.retrieving_files = RetrievingFiles()
        self.consumer = get_consumer('podcast_file_metadata')

    def preparing_the_data_parts(self, meta_record):
        id = self.unique_id_generator.generates_id_from_metadata(meta_record)
        file = self.retrieving_files.content_in_binary_form(meta_record)

        return id , file

    def run(self):
        for record in self.consumer:
            meta_record = record.value
            id , file = self.preparing_the_data_parts(meta_record)

        self.consumer.close()