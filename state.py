import os
from pathlib import Path


_BASE_DIR = Path(__file__).resolve().parent
PROJECT_PATH = os.path.join(str(_BASE_DIR), "")
DATA_PATH = str(_BASE_DIR / "config.json")
