import joblib
from pathlib import Path
import pandas as pd

class PredictionPipeline:
    def __init__(self):
        self.preprocessor = joblib.load(Path("artifacts/data_transformation/preprocessor.joblib"))
        self.model = joblib.load(Path("artifacts/model_trainer/best_model.joblib"))

    def predict(self, data: pd.DataFrame):
        preprocessed_data = self.preprocessor.transform(data)
        prediction = self.model.predict(preprocessed_data)

        return prediction
