"""
file_manager.py

Provides classes for file-based data transactions and entity management.
Handles directory creation, reading, writing, modifying, and deleting JSON data files,
as well as building and updating entity datasets for the E-Commerce Mascotas API.
"""

import json
import os
from pathlib import Path
from validators.validator import dir_or_file_exists
from validators.schema_validator import schemas, schema_builder_for_new_registrations, schema_validator
from configurations.config import directory_list, default_table_templates, directory_mapper
from datetime import datetime
import uuid
import pprint

class FileTransactions:
    """
    Handles file-based transactions for reading, writing, modifying, and deleting JSON data.
    Also manages directory creation and loading all JSON files from a directory.
    """

    def __init__(self):
        """
        Initialize FileTransactions with the list of required directories.
        """
        self.dir_list = directory_list
        
    def create_directories(self):
        """
        Create all directories required for the application if they do not exist.
        """
        for path in self.dir_list:
            Path(path).mkdir(exist_ok=True)
    
    def load_all_json_files(self, directory_path):
        """
        Load all JSON files from a directory.

        Args:
            directory_path (str): Path to the directory.

        Returns:
            list: List of data loaded from JSON files.
        """
        data = []
        for file_path in Path(directory_path).glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data.append(json.load(f))
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON: {file_path.name} - {e}")
        return data

    def read_data(self, filepath_name):
        """
        Read data from a JSON file.

        Args:
            filepath_name (str): Path to the JSON file.

        Returns:
            dict: Data loaded from the JSON file, or None if file does not exist.
        """
        true_false = dir_or_file_exists(filepath_name, option="File")
        if true_false:
            with open(filepath_name, "r", encoding="utf-8") as file:
                return json.load(file)
    
    def write_data(self, data, filepath_name, option="w", var_name=None):
        """
        Write data to a file (JSON or Python).

        Args:
            data (dict): Data to write.
            filepath_name (str): Path to the file.
            option (str): File open mode (default "w").
            var_name (str, optional): Variable name for Python files.

        Returns:
            bool: True if file already exists, False otherwise.
        """
        true_false = dir_or_file_exists(filepath_name)
        if true_false:
            return true_false
        if true_false is False:
            with open(filepath_name, option, encoding='utf-8') as file:
                if filepath_name.endswith(".py"):
                    file.write(f"{var_name} = ")
                    file.write(pprint.pformat(data.get(var_name), indent=4))
                    file.write("\n\n")
                else:
                    json.dump(data, file, indent=4)
            return true_false

    def modify_data(self, data, filepath_name):
        """
        Modify existing data in a JSON file.

        Args:
            data (dict): Data to update.
            filepath_name (str): Path to the JSON file.

        Returns:
            tuple: (bool, dict) True if file exists, and the updated data.
        """
        true_false = dir_or_file_exists(filepath_name, option="File")
        current_data = self.read_data(filepath_name)
        if true_false:
            current_keys = current_data.keys()
            for k, v in data.items():
                if k in current_keys:
                    current_data[k] = v
            with open(filepath_name, 'w', encoding='utf-8') as file:
                json.dump(current_data, file, indent=4)
            return true_false, current_data
        return true_false, current_data

    def delete_data(self, filepath_name):
        """
        Delete a JSON file.

        Args:
            filepath_name (str): Path to the JSON file.

        Returns:
            tuple: (bool, int) True if file existed and was deleted, and HTTP status code.
        """
        true_false = dir_or_file_exists(filepath_name, option="File")
        if true_false:
            Path(filepath_name).unlink()
            return true_false, 200
        return true_false, 404

class EntityDatasetManager:
    """
    Manages entity datasets, including filtering, creating, and building entities
    based on templates and schemas for the application.
    """

    def __init__(self):
        """
        Initialize EntityDatasetManager with schemas, templates, and file transaction handler.
        """
        self.schemas = schemas
        self.data = []
        self.directory_mapper = directory_mapper
        self.templates = default_table_templates
        self.file_transaction = FileTransactions()

    def filter_new_entity_data(self, files_content, option):
        """
        Filter and build new entity data using the schema builder.

        Args:
            files_content (list): List of data items.
            option (str): Entity type/schema name.
        """
        for data in files_content:
            result = schema_builder_for_new_registrations(_schema=option, data_content=data)
            self.data.append(result)

    def create_entity(self, option, id):
        """
        Create a new entity file from a template and data.

        Args:
            option (str): Entity type/schema name.
            id (str): Entity ID.
        """
        template = self.templates.get(option)
        data_content = self.data
        dir_path = self.directory_mapper.get(option)
        for data in data_content:
            template.update(data)
            template['id'] = id
            template['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
            template['status'] = "disable"
            filepath_name = f"{dir_path}/{template.get('id')}.json"
            _ = self.file_transaction.write_data(template, filepath_name)

    def schema_entity_builder(self, _schema=None, id=None, data_content={}):
        """
        Build and save an entity using a schema, ID, and data content.

        Args:
            _schema (str, optional): Schema name/entity type.
            id (str, optional): Entity ID.
            data_content (dict, optional): Data to populate the entity.

        Returns:
            None
        """
        dataset = self.templates.get(_schema)
        dir_path = self.directory_mapper.get(_schema)
        filepath_name = f"{dir_path}/{id}.json"
        for k, v in data_content.items():
            if k in self.schemas[_schema]().load_fields.keys():
                dataset.update({k: v})
                if _schema == "sales" and data_content.get("checkout") == "False":
                    dataset['id'] = id
                    dataset['receipt_id'] = data_content.get("receipt_id")
                    dataset['cart_id'] = data_content.get("id")
                    dataset['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
                    dataset['status'] = "pending_payment" 
                elif _schema == "sales" and data_content.get("checkout") == "True":
                    dataset['id'] = id
                    dataset['receipt_id'] = data_content.get("receipt_id")
                    dataset['cart_id'] = data_content.get("id")
                    dataset['purchase_date'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
                    dataset['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
                    dataset['status'] = "completed_payment"
                elif _schema == "receipts" and data_content.get("checkout") == "False":
                    dataset['id'] = id
                    dataset['receipt_number'] = str(uuid.uuid4())
                    dataset['cart_id'] = data_content.get("id")
                    dataset['sale_id'] = data_content.get("sale_id")
                    dataset['products'] = data_content.get("products")
                    dataset['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
                elif _schema == "receipts" and data_content.get("checkout") == "True":
                    dataset['id'] = id
                    dataset['cart_id'] = data_content.get("id")
                    dataset['sale_id'] = data_content.get("sale_id")
                    dataset['products'] = data_content.get("products")
                    dataset['purchase_date'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
                    dataset['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
                    dataset['total_amount'] = 0
        schema_true, msg = schema_validator(_schema, dataset)
        if schema_true:
            _ = self.file_transaction.write_data(dataset, filepath_name)