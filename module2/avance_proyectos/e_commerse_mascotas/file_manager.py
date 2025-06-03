import json
import os
from pathlib import Path
from config import (
    ROOT_DIR, DB_DIR, REGISTRATIONS_DIR,
    ROLES_DIR, USERS_DIR, INVENTORY_DIR,
    SALES_DIR, PRODUCTS_DIR,
    USERS_REGISTRATION_DIR, PRODUCT_REGISTRATION_DIR
)


class UserValidator:
    def __init__(self):
        pass
    
    def user_is_registered(self):
        pass
    
    def is_email(self):
        pass
    
    def is_admin(self):
        pass


class DataValidator:
    def __init__(self):
        pass
    
    def valid_fields_name(self):
        pass
    
    def valid_fields_type(self):
        pass


class FileValidator:
    def __init__(self):
        pass
        
    def dir_exists(self, filepath):
        dir_path = Path(path)
        # Check if directory exists
        if dir_path.exists():
            print("Directory exists")
            return True
        return False
    
    def file_exist(self, filename):
        file_path = Path(filename)
        # Check if directory exists
        if file_path.exists():
            print("File exists.")
            return True
        return False
    
    def create_dir(self, dir):
        pass
    
    def is_dict(self):
        pass
    
    def is_json(self):
        pass


class FileTransactions:
    def __init__(self):
        self.file_validator = FileValidator()
        self.root_dir = ROOT_DIR
        self.db_dir = DB_DIR
        self.registration_dir = REGISTRATIONS_DIR
        self.users_registration_dir = USERS_REGISTRATION_DIR
        self.products_registration_dir = PRODUCT_REGISTRATION_DIR
        self.roles_dir = ROLES_DIR
        self.users_dir = USERS_DIR
        self.inventory_dir = INVENTORY_DIR
        self.sales_dir = SALES_DIR
        self.products_dir = PRODUCTS_DIR
        self.dir_list = [
            self.root_dir, self.db_dir, self.registration_dir,
            self.users_registration_dir, self.products_registration_dir,
            self.roles_dir, self.users_dir, self.inventory_dir,
            self.sales_dir, self.products_dir
        ]
        
    def create_directories(self):
        for path in self.dir_list:
            Path(path).mkdir(exist_ok=True)
    
    def load_all_json_files(self, directory_path):
        data = []
        for file_path in Path(directory_path).glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data.append(json.load(f))
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON: {file_path.name} - {e}")
        return data

    def read_data(self, filepath_name):
        with open(filepath_name, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def write_data(self, data, filepath_name):
        true_false = self.file_validator.file_exist(filepath_name)
        if true_false:
            return true_false
        if true_false is False:
            with open(filepath_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            return true_false
    
    def modify_data(self, data, filepath_name):
        true_false = self.file_validator.file_exist(filepath_name)
        current_data = self.read_data(filepath_name)
        if true_false:
            current_keys = current_data.keys()
            for k,v in data.items():
                if k in current_keys:
                    current_data[k] = v
            with open(filepath_name, 'w', encoding='utf-8') as file:
                json.dump(current_data, file, indent=4)
            return true_false, current_data
        return true_false, current_data

    def delete_data(self, filepath_name):
        true_false = self.file_validator.file_exist(filepath_name)
        if true_false:
            Path(filepath_name).unlink()
            return true_false, 200
        return true_false, 404