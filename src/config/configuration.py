from src.constants import *
from src.utils import read_yaml, create_directories
from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig
)

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
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.DataValidation
        # schema = self.schema.columns
        schema = self.schema
        
        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            unzipped_data_dir=config.unzipped_data_dir,
            status_file_path=config.status_file_path,
            all_schema=schema.columns,
            target_column=schema.target_column
        )
        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.DataTransformation
        schema = self.schema

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            unzipped_data_dir=config.unzipped_data_dir,
            train_data=config.train_data,
            test_data=config.test_data,
            preprocessor_path=config.preprocessor_path,
            target_variable=schema.target_column,
            status_file_path=config.status_file_path,
        )

        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.ModelTrainer
        params = self.params.params.to_dict()

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_dir=config.train_data_dir,
            model_path=config.model_path,
            params=params,
        )

        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.ModelEvaluation

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_dir=config.test_data_dir,
            model_path=config.model_path,
            metric_file_name=config.metric_file_name,
        )
        return model_evaluation_config
    
    
    

