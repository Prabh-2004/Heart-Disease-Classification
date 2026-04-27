from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    zipped_file_dir: Path
    unzipped_file_path: Path

@dataclass
class DataValidationConfig:
    root_dir: Path
    unzipped_data_dir: Path
    status_file_path: Path
    all_schema: dict
    target_column: str
    
@dataclass
class DataTransformationConfig:
    root_dir: Path
    unzipped_data_dir: Path
    train_data: Path
    test_data: Path
    target_variable: str
    preprocessor_path: Path
    status_file_path: Path

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    processed_data_dir: Path
    model_path: Path
    params: dict

@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    x_test_data_path: Path
    y_test_data_path: Path
    model_path: Path