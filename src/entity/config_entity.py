from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    zipped_file_dir: Path
    unzipped_file_path: Path

    