from src.entity.config_entity import DataValidationConfig
from src.config.configuration import ConfigurationManager
from src.logging import logger
import pandas as pd


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def check_columns(self, data) -> bool:
        data_cols = set(data.columns) - {self.config.target_column}
        schema_cols = set(self.config.all_schema.keys())

        if data_cols == schema_cols:
            return True
        else:
            logger.info(f"Missing: {schema_cols - data_cols}, Extra: {data_cols - schema_cols}")
            return False

    def check_datatype(self, data) -> bool:
        for col, expected_type in self.config.all_schema.items():
            if col not in data.columns:
                return False

            # if str(data[col].dtype) != str(expected_type):
            #     logger.info(f"Datatype mismatch in {col}")
            #     return False

        return True

    def validate_data(self):
        data = pd.read_csv(self.config.unzipped_data_dir)

        validate_columns = self.check_columns(data)
        validate_datatype = self.check_datatype(data)

        target_present = self.config.target_column in data.columns

        if not target_present:
            logger.info("Target column missing")

        validation_status = validate_columns and validate_datatype and target_present

        with open(self.config.status_file_path, 'w') as file:
            file.write(f"Validation Status: {validation_status}")

        logger.info(f"Validation Status: {validation_status}")
        