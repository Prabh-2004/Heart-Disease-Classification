from src.logging import logger
from src.config.configuration import ConfigurationManager
from src.components.model_trainer import ModelTrainer


class ModelTrainingPipeline:
    def __init__(self):
        pass

    def initiate_model_training(self):
        try:
            config = ConfigurationManager()
            model_training_config = config.get_model_trainer_config()
            model_training = ModelTrainer(config=model_training_config)
            model_training.train_model()
        except Exception as e:
            raise e