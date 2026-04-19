from src.config.configuration import ConfigurationManager
from src.entity.config_entity import DataIngestionConfig
from src.logging import logger
import os, zipfile
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_data(self):
        # create the directory for the zipped data
        os.makedirs(self.config.zipped_file_dir, exist_ok=True)

        # load the data from kaggle cli
        download_status = os.system(f"kaggle datasets download -d {self.config.source_url} -p {self.config.zipped_file_dir}")
        if download_status == 1:
            logger.info("Data couldn't get downloaded. Please check your url.")
        
        if download_status==0:
            logger.info(f"Data successfully downloaded at: {self.config.zipped_file_dir}.")

    def extract_data(self):
        zip_file_name = os.listdir(path=self.config.zipped_file_dir)[0]
        unzip_dir, unzipped_filename = os.path.split(self.config.unzipped_file_path)

        if unzipped_filename not in os.listdir(self.config.root_dir):
            # unzip the data
            with zipfile.ZipFile(os.path.join(self.config.zipped_file_dir, zip_file_name)) as zip_ref:
                zip_ref.extractall(unzip_dir)

        # change the name of the unzipped file.

        for item in os.listdir(self.config.root_dir):

            if ".csv" in item:
                old_name = os.path.join(self.config.root_dir, item)
                new_name = os.path.join(self.config.root_dir, unzipped_filename)
                os.rename(old_name, new_name)
            
        logger.info(f"Successfully loaded data {unzipped_filename} at location: {unzip_dir}")
        
        
