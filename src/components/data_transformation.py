from src.logging import logger
from src.entity.config_entity import DataTransformationConfig
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import joblib


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def split_data(self, data: pd.DataFrame):
        X = data.drop([self.config.target_variable], axis=1)
        y = data[self.config.target_variable]

        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=67)

        return X_train, X_test, y_train, y_test
    
    
    def preprocessor(self, data: pd.DataFrame):
        numerical_features = np.array(data.select_dtypes(['int64', 'float64']).columns)
        categorical_features = np.array(data.select_dtypes(['object']).columns)

        numerical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy='median')),
            ("scaler", StandardScaler()),
        ])

        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy='most_frequent')),
            ("encoder", OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
        ])

        preprocessor = ColumnTransformer([
            ("categorical", categorical_pipeline, categorical_features),
            ("numerical", numerical_pipeline, numerical_features),
        ])
        
        return preprocessor
    
    
    def transform_data(self):
        with open(self.config.status_file_path, 'r') as file:
            content = file.read()

        if content.split()[-1] == "True":
            try:
                data = pd.read_csv(self.config.unzipped_data_dir)
                # remove duplicated values
                data.drop_duplicates(inplace=True)
                # train-test split
                X_train, X_test, y_train, y_test = self.split_data(data)

                preprocessor_obj = self.preprocessor(X_train)

                X_train_values = preprocessor_obj.fit_transform(X_train)
                X_test_values = preprocessor_obj.transform(X_test)

                feature_names = preprocessor_obj.get_feature_names_out()

                X_train = pd.DataFrame(data=X_train_values, columns=feature_names)
                X_test = pd.DataFrame(data=X_test_values, columns=feature_names)

                logger.info("Dataset successfully transformed.")

                # save the processed training and testing data

                os.makedirs(self.config.train_data, exist_ok=True)
                os.makedirs(self.config.test_data, exist_ok=True)

                X_train.to_csv(os.path.join(self.config.train_data, "x_train.csv"), index=False)
                y_train.to_csv(os.path.join(self.config.train_data, "y_train.csv"), index=False)
                X_test.to_csv(os.path.join(self.config.test_data, "x_test.csv"), index=False)
                y_test.to_csv(os.path.join(self.config.test_data, "y_test.csv"), index=False)

                logger.info(f"Training Data successfully saved at: {self.config.train_data}.")
                logger.info(f"Test Data successfully saved at: {self.config.test_data}.")

                # save the preprocessor model
                preprocessor_dir, preprocessor_path = os.path.split(self.config.preprocessor_path)

                os.makedirs(preprocessor_dir, exist_ok=True)
                joblib.dump({
                    "preprocessor": preprocessor_obj,
                    "feature_name": feature_names,
                }, self.config.preprocessor_path)
                logger.info(f"Saved preprocessor at: {self.config.preprocessor_path}")

            except Exception as e:
                logger.exception(e)
                raise e
            
        else:
            logger.exception(f"Data is not Valid. Data Transformation Failed.")
