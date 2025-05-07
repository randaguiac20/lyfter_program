import csv
import os
import shutil


def load_finance_data(filename="data/my_finance_data.csv"):
    finance_info = []
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            finance_info = [row for row in reader if len(row) == 4]
        return finance_info[0], finance_info[1:]
    except FileNotFoundError:
        print("sNo information available at the moment.")

def load_category_data(filename="data/categories.txt"):
    if not os.path.exists(filename):
        # Create the file
        with open(filename, 'w') as file:
            file.write("")  
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().strip().split("\n")

def add_category(value, filename="data/categories.txt"):
    content = 0
    try:
        if os.path.getsize(filename):
            content = os.path.getsize(filename)
    except FileNotFoundError:
        content = 0
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{value}\n")

def write_finance_data(dataset, headers=None,
                       filename="my_finance_data.csv"):
    content = 0
    data_dir = "data/"
    file_path = os.path.join(data_dir, filename)
    try:
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        if os.path.getsize(file_path):
            content = os.path.getsize(file_path)
    except FileNotFoundError:
        content = 0
    with open(file_path, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        if content == 0:
            writer.writerow(headers)
            writer.writerows(dataset)
        else:
            writer.writerows(dataset)

def export_csv_records(filename="exported_finance_data.csv"):
    src_file = "data/my_finance_data.csv"
    destination_file = f"data/{filename}"
    if not os.path.exists(destination_file):
        print(f"\nCreating file {filename}.")
        with open(destination_file, 'w') as file:
            file.write("")
    shutil.copy(src_file, destination_file)
    print(f"\nFile {filename} succesfully updated!")
