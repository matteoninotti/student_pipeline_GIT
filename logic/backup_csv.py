from shutil import copy
from .ETL import csv_file_name, now_time
from ..main import PROJECT_PATH



bkup_file_name = PROJECT_PATH + "data/backup/backup_studenti_" + now_time + ".csv"

copy(csv_file_name, bkup_file_name)

