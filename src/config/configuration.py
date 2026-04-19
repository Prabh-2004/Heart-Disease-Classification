from src.constants import *
from src.utils import read_yaml, create_directories
from src.entity.config_entity import (DataIngestionConfig)

class ConfigurationManager:
    def __init__(self, config_file=CONFIG_FILE_PATH, params_file=PARAMS_FILE_PATH, schema_file=SCHEMA_FILE_PATH):
        self.config = read_yaml(config_file)
        self.params = read_yaml(params_file)
        self.schema = read_yaml(schema_file)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.DataIngestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            zipped_file_dir=config.zipped_file_dir,
            unzipped_file_path=config.unzipped_file_path,
        )

        return data_ingestion_config
    
