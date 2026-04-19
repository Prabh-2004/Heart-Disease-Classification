from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
import yaml, os
from src.logging import logger

@ensure_annotations
def read_yaml(file_path: Path) -> ConfigBox:
    try:
        with open(file_path, "r") as yaml_file:
            data = yaml.safe_load(yaml_file)
            logger.info(f"yaml file {file_path} loaded successfully.")
        return ConfigBox(data)
    except BoxValueError:
        raise ValueError("yaml file is empty.")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(paths: list):
    try:
        for path in paths:
            os.makedirs(path, exist_ok=True)
            logger.info(f"directory {path} created successfully.")
    except Exception as e:
        raise e
    

