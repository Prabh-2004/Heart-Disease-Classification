from src.logging import logger
from src.pipelines.data_ingestion_pipeline import DataIngestionPipeline
from src.pipelines.data_validation_pipeline import DataValidationPipeline
from src.pipelines.data_transformation_pipeline import DataTransformationPipeline
from src.pipelines.model_trainer_pipeline import ModelTrainingPipeline


STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.initiate_data_ingestion()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Validation Stage"
try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    data_validation = DataValidationPipeline()
    data_validation.initiate_data_validation()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Transformation Stage"   
try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    data_transformation = DataTransformationPipeline()
    data_transformation.initiate_data_transformation()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x") 
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Model Training Stage"   
try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    model_trainer = ModelTrainingPipeline()
    model_trainer.initiate_model_training()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x") 
except Exception as e:
    logger.exception(e)
    raise e
