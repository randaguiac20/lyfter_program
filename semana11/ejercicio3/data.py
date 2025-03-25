import os
import csv
import shutil

def extract_keys_structure(headers):
    clean_dataset = []
    for key in headers.keys():
        if isinstance(headers[key], str):
            clean_dataset.append(key)
        if isinstance(headers[key], int):
            clean_dataset.append(key)
    return clean_dataset


def transform_dict_to_csv(student_records):
    header_string = "name,class,spanish_grade,english_grade,history_grade,science_grade"
    row_list = []
    row_string = ""
    if student_records is not None:
        for _, student_record in student_records.items():
            for _, value in student_record.items():
                row_string += f"{value},"
            row_list.append(row_string[0:-1])
        row_list.insert(0, header_string)
        return row_list
    else:
        return None


def write_student_info(dataset, filename="student_info.csv"):
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
            csv_writter.writerows([dataset])
        else:
            csv_writter.writerows([dataset])


def load_as_csv(filename="student_info.csv"):
    student_info = []
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            data = csv.reader(file, delimiter=',')
            for rows in data:
                student_data = ', '.join(rows)
                student_info.append(student_data)
            return student_info
    except FileNotFoundError:
        print("")

def load_csv_as_dict(filename="student_info.csv"):
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


def export_csv_records(filename="exported_student_info.csv"):
    src_file = "student_info.csv"
    destination_file = filename
    try:
        shutil.copy(src_file, destination_file)
        print("\nFile succesfully exported!")
    except FileNotFoundError:
        print("\nUnable to export the file, because there is not data available yet!!")


def import_csv_records(filename="exported_student_info.csv"):
    try:
        if os.path.getsize(filename):
            student_info = load_as_csv(filename=filename)
            return student_info
    except FileNotFoundError:
        print("\nFile does not exist, no previous file has been exported.")
        