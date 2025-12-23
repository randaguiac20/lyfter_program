import csv
import os
import shutil
from env_vars import (HEADERS, TASKS_FILENAME,
                      DATA_DIR, DATA_DIR_FILENAME)
from validator import check_file_not_found


class Transaction:
    def __init__(self):
        self.data_dir = os.mkdir(DATA_DIR) if not os.path.exists(DATA_DIR) else DATA_DIR

    @check_file_not_found(create_if_missing=True, file_type="csv", headers=HEADERS)
    def read_csv_file(self, filename=DATA_DIR_FILENAME):
        with open(filename, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)
            return data

    def write_csv_file(self, filename=DATA_DIR_FILENAME,
                       dataset=[], write_option="a"):
        with open(filename, write_option, encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            try:
                content_size = os.path.getsize(filename)
            except FileNotFoundError:
                content_size = 0
            if content_size == 0:
                writer.writerow(HEADERS)
                writer.writerows(dataset)
            else:
                writer.writerows(dataset)
