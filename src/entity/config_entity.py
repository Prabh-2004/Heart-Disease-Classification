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
    train_file_path: Path
    test_file_path: Path
    target_variable: str
    preprocessor_path: Path
    status_file_path: Path