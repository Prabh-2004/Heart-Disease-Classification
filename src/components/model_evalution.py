import os, mlflow, joblib, json
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report
from dotenv import load_dotenv
load_dotenv()

from src.logging import logger
from src.entity.config_entity import ModelEvaluationConfig

os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def evaluate_model(self):
        model_file = os.path.join(self.config.model_path, "best_model.joblib")
        model = joblib.load(model_file)

        x_test = pd.read_csv(os.path.join(self.config.test_data_dir, "x_test.csv"))
        y_test = pd.read_csv(os.path.join(self.config.test_data_dir, "y_test.csv"))
        y_test = y_test.values.ravel()

        y_pred = model.predict(x_test)

        f1 = f1_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        cr = classification_report(y_test, y_pred)

        metrics = {
            "F1 Score": f1,
            "Accuracy Score": accuracy, 
        }

        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
        mlflow.set_experiment(experiment_name="Best Model Evaluation")

        with mlflow.start_run(run_name="Model Testing"):
            mlflow.log_metric("F1 Score", f1)
            mlflow.log_metric("Accuracy Score", accuracy)
            mlflow.log_text(text=str(cm), artifact_file="confusion_matrix.txt")
            mlflow.log_text(text=str(cr), artifact_file="classification_report.txt")

        with open(self.config.metric_file_name, 'w') as file:
            json.dump(metrics, file, indent=4)
        
        logger.info(f"Metrics.json file saved at {self.config.metric_file_name}.")


        

