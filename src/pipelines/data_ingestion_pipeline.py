from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.logging import logger

class DataIngestionPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.extract_data()
        except Exception as e:
            logger.exception(e)
            raise e


