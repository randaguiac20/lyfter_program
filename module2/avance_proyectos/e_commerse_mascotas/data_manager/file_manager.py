import json
import os
from pathlib import Path
from validators.validator import dir_or_file_exists
from validators.schema_validator import schema_builder_for_new_registrations,schema_validator
from configurations.config import directory_list,default_table_templates,directory_mapper
from datetime import datetime
import uuid


class FileTransactions:
    def __init__(self):
        self.dir_list = directory_list
        
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
        true_false = dir_or_file_exists(filepath_name, option="File")
        if true_false:
            with open(filepath_name, "r", encoding="utf-8") as file:
                return json.load(file)
    
    def write_data(self, data, filepath_name):
        true_false = dir_or_file_exists(filepath_name)
        if true_false:
            return true_false
        if true_false is False:
            with open(filepath_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            return true_false

    def modify_data(self, data, filepath_name):
        true_false = dir_or_file_exists(filepath_name, option="File")
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
        true_false = dir_or_file_exists(filepath_name, option="File")
        if true_false:
            Path(filepath_name).unlink()
            return true_false, 200
        return true_false, 404

class EntityDatasetManager:
    def __init__(self):
        self._schema = schema_validator
        self.data = []
        self.templates = default_table_templates
        self.file_transaction = FileTransactions()

    def filter_new_entity_data(self, files_content, option):
        schema_option = option.split("_")[0]
        for data in files_content:
            result = schema_builder_for_new_registrations(_schema=schema_option, data_content=data)
            self.data.append(result)

    def create_entity(self, option, id):
        template = self.templates.get(option)
        data_content = self.data
        dir_path = directory_mapper.get(option)
        for data in data_content:
            template.update(data)
            template['id'] = id
            template['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
            template['status'] = "disable"
            filepath_name = f"{dir_path}/{template.get('id')}.json"
            _ = self.file_transaction.write_data(template, filepath_name)
