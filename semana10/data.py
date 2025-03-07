import os
import csv

def extract_keys_structure(headers):
    clean_dataset = []
    for key in headers[0].keys():
        if isinstance(headers[0][key], str):
            clean_dataset.append(key)
        if isinstance(headers[0][key], int):
            clean_dataset.append(key)
    return clean_dataset


def write_student_info(dataset, filename="student_info.txt"):
    headers = extract_keys_structure(dataset)
    content = 0
    try:
        if os.path.getsize(filename):
            content = os.path.getsize(filename)
    except FileNotFoundError:
        content = 0
    with open(filename, 'a', encoding='utf-8') as file:
        csv_writter = csv.DictWriter(file, headers)
        if content == 0:
            csv_writter.writeheader()
            csv_writter.writerows(dataset)
        else:
            csv_writter.writerows(dataset)


def show_as_csv(filename="student_info.txt"):
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            data = csv.reader(file, delimiter=',')
            for rows in data:
                print(', '.join(rows))
    except FileNotFoundError:
        print("No information available at the moment.")

def convert_csv_to_dict(filename="student_info.txt"):
    dict_data = {}
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            data = csv.DictReader(file, delimiter=',')
            for rows in data:
                pkey = rows["name"]
                dict_data.update({pkey: {}})
                for key, value in rows.items():
                    dict_data[pkey].update({key: value})
        if len(dict_data) == 0:
            print("\nThere are not records in the system yet.")
        else:
            return dict_data
    except FileNotFoundError:
        print("\nThere are not records in the system yet.")