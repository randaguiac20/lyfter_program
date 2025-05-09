import csv
import os
import shutil
from env_vars import (FINANCE_FILENAME, CATEGORIES_FILENAME,
                      EXPORTED_FINANCE_FILENAME, DATA_DIR,
                      DATA_DIR_FINANCE_FILENAME,
                      DATA_DIR_CATEGORIES_FILENAME,
                      DATA_DIR_EXPORTED_FINANCE_FILENAME,
                      HEADERS)
from validator import check_file_not_found


class DataManager:
    def __init__(self):
        self.data_dir = os.mkdir(DATA_DIR) if not os.path.exists(DATA_DIR) else DATA_DIR

    @check_file_not_found(create_if_missing=True, file_type="csv", headers=HEADERS)
    def read_csv_file(self, finance_filename=DATA_DIR_FINANCE_FILENAME):
        with open(finance_filename, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            data = list(reader)
            return data
    
    @check_file_not_found(create_if_missing=True, file_type="txt")
    def read_txt_file(self, categories_filename=DATA_DIR_CATEGORIES_FILENAME):
        with open(categories_filename, "r", encoding="utf-8") as file:
            reader = file.read().strip().split("\n")
            return reader

    def write_csv_file(self, finance_filename=DATA_DIR_FINANCE_FILENAME,
                       dataset=[]):
        with open(finance_filename, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            try:
                content_size = os.path.getsize(finance_filename)
            except FileNotFoundError:
                content_size = 0
            if content_size == 0:
                writer.writerow(HEADERS)
                writer.writerows(dataset)
            else:
                writer.writerows(dataset)

    def write_txt_file(self, categories_filename=DATA_DIR_CATEGORIES_FILENAME,
                       value=None):
        with open(categories_filename, 'a', encoding='utf-8') as file:
            file.write(f"{value}\n")

    @check_file_not_found()
    def export_csv_file(self, finance_filename=DATA_DIR_FINANCE_FILENAME, 
                    export_finance_filename=DATA_DIR_EXPORTED_FINANCE_FILENAME):
        shutil.copy(finance_filename, export_finance_filename)
        print(f"\nFile {export_finance_filename} succesfully updated!")
