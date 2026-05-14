import os
from shutil import copy
from .ETL import csv_file_name, now_time
from ..main import PROJECT_PATH



bkup_file_name = os.path.join(PROJECT_PATH, "data", "backup", f"backup_studenti_{now_time}.csv")

copy(csv_file_name, bkup_file_name)
