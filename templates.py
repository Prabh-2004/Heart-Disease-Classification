import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_directories = [
    f"src/__init__.py",
    f"src/components/__init__.py",
    f"src/config/__init__.py",
    f"src/config/configuration.py",
    f"src/utils/__init__.py",
    f"src/entity/__init__.py",
    f"src/entity/config_entity.py",
    f"src/pipelines/__init__.py",
    f"src/constants/__init__.py",
    f"src/logging/__init__.py",
    f"config/config.yaml",
    "config/params.yaml",
    "config/schema.yaml",
    "notebooks/test.ipynb",
    "main.py",
    "Dockerfile",
    ".dockerignore",
    "app.py",
    "setup.py"  
]

for directory in list_of_directories:
    filepath = Path(directory)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Successfully created directory: {filedir} for the file: {filedir}")

    if (not os.path.exists(filepath) or os.path.getsize(filepath) == 0):
        with open(filepath, "w") as file:
            pass

        logging.info(f"Successfully created empty file at: {filepath}")
    else:
        logging.info(f"The File {filepath} already exists.")


