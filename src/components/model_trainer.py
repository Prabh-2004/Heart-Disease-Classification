from src.entity.config_entity import ModelTrainerConfig
from src.logging import logger
import os
import mlflow
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
import joblib
from urllib.parse import urlparse

from dotenv import load_dotenv
load_dotenv()

os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_TRACKING_URI")
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train_model(self):
        x_train = pd.read_csv(os.path.join(self.config.train_data_dir, "x_train.csv"))
        y_train = pd.read_csv(os.path.join(self.config.train_data_dir, "y_train.csv"))
        y_train = y_train.values.ravel()

        models = {
            "SVC": SVC(),
            "RandomForestClassifier": RandomForestClassifier(),
            "XGBClassifier": XGBClassifier()
        }

        model_scores = {}
        best_model = None
        best_score = -np.inf
        best_model_name = None

        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
        mlflow.set_experiment(experiment_name="Heart Disease Prediction Model")

        with mlflow.start_run(run_name="Model Training"):
            for model_name, model in models.items():
            
                with mlflow.start_run(run_name=model_name, nested=True):
                    gs = GridSearchCV(
                        estimator=model,
                        param_grid=self.config.params[model_name],
                        cv=3,
                        scoring="f1",
                        n_jobs=-1,
                        verbose=True,
                    )

                    gs.fit(x_train, y_train)

                    mlflow.log_params(gs.best_params_)
                    mlflow.log_metric("best_f1", gs.best_score_)

                    # mlflow.sklearn.log_model(sk_model=gs.best_estimator_, name=model_name)

                    model_scores[model_name] = gs.best_score_

                    if gs.best_score_ > best_score:
                        best_score = gs.best_score_
                        best_model = gs.best_estimator_
                        best_model_name = model_name

            mlflow.log_param("best_model_name", best_model_name)
            mlflow.log_metric("best_model_f1", best_score)
            
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(
                    sk_model=best_model,
                    artifact_path=best_model_name,
                    registered_model_name=f"Best Model - {best_model_name}"
                )
            else:
                mlflow.sklearn.log_model(
                    sk_model=best_model,
                    artifact_path=best_model_name
                )

        logger.info(f"Best Model: {best_model_name} with f1 score: {best_score}")
        model_path = os.path.join(self.config.model_path, "best_model.joblib")
        joblib.dump(best_model, model_path)
        logger.info(f"Best Model saved at: {model_path}")

