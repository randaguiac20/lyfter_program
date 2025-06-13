"""
db_connector.py

Provides the DataManager class for handling data operations such as CRUD,
admin user creation, and entity management for the E-Commerce Mascotas API.
Interacts with the file system to simulate a database using JSON files.
"""

from datetime import datetime
from configurations.config import (directory_mapper, admin_user, USERS_DIR, ROLES_DIR)
from data_manager.file_manager import FileTransactions, EntityDatasetManager
from validators.validator import content_mapper
from aaa.authentication import generate_password

class DataManager:
    """
    Handles data operations for the application, including CRUD, admin user creation,
    and entity management. Uses JSON files to simulate database tables.
    """

    def __init__(self):
        """
        Initialize DataManager with file and entity managers and directory mapping.
        """
        self.query_file = FileTransactions()
        self.entity_dm = EntityDatasetManager()
        self.directory_mapper = directory_mapper
    
    def create_admin_data(self):
        """
        Create the default admin user if it does not exist.

        Sets up the admin user's password, status, and last modified date,
        and writes the admin user data to the users directory.
        """
        password = generate_password(admin_user)
        admin_user['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        admin_user['password'] = password
        admin_user['status'] = "active"
        _ = self.query_file.write_data(admin_user, f"{USERS_DIR}/admin_user.json")

    def get_data_item(self, id):
        """
        Retrieve a single data item by its file path.

        Args:
            id (str): Path to the JSON file.

        Returns:
            tuple: (data, int) Data and HTTP status code (200 if found, 404 if not).
        """
        data = self.query_file.read_data(id)
        if data:
            return data, 200
        return data, 404
    
    def get_data_by_email(self, directory_path, email, admin=None):
        """
        Retrieve a user by email from a directory.

        Args:
            directory_path (str): Directory to search.
            email (str): Email address to look up.
            admin (optional): Not used.

        Returns:
            tuple: (dict or list, int) User data and HTTP status code.
                   200 if active, 400 if not active, 404 if not found.
        """
        data, http_code = self.get_data_items(directory_path)
        user_data = [d for d in data if d.get("email") == email]
        if user_data[0].get("status") == "active":
            return user_data[0], http_code
        if user_data[0].get("status") != "active":
            return user_data, 400
        return user_data, 404

    def get_data_items(self, directory_path):
        """
        Retrieve all data items from a directory.

        Args:
            directory_path (str): Directory to load JSON files from.

        Returns:
            tuple: (list, int) List of data items and HTTP status code (200).
        """
        data = self.query_file.load_all_json_files(directory_path)
        return data, 200
            
    def save_data(self, request_data, filepath, directory_path, option):
        """
        Save a new data item, handling entity creation and validation.

        Args:
            request_data (dict): Data to save.
            filepath (str): Path to save the JSON file.
            directory_path (str): Directory for the entity.
            option (str): Entity type.

        Returns:
            tuple: (dict, int) Response message and HTTP status code.
        """
        files_data = self.query_file.load_all_json_files(directory_path)
        data_exist = content_mapper(files_data, request_data, option)
        if data_exist:
            return {"message": f"{option} ID under {request_data.get('id')} already exist."}, 403
        true_false = self.query_file.write_data(request_data, filepath)
        files_data = self.query_file.load_all_json_files(directory_path)
        if option == "carts":
            sale_id = request_data.get("sale_id")
            self.entity_dm.schema_entity_builder("sales", sale_id, request_data)
            receipt_id = request_data.get("receipt_id")
            self.entity_dm.schema_entity_builder("receipts", receipt_id, request_data)
        if option == "product_registration":
            self.entity_dm.filter_new_entity_data(files_data, "inventory")
            inventory_id = request_data.get("inventory_id")
            self.entity_dm.create_entity("inventory", inventory_id)
            self.entity_dm.filter_new_entity_data(files_data, "products")
            product_id = request_data.get("product_id")
            self.entity_dm.create_entity("products", product_id)
        if option == "user_registration":
            self.entity_dm.filter_new_entity_data(files_data, "users")
            user_id = request_data.get("user_id")
            self.entity_dm.create_entity("users", user_id)
        if true_false:
            return {"message": f"{option} ID {request_data.get('id')} already exist."}, 403
        return {"message": f"{option} ID {request_data.get('id')} has been registered."}, 200
    
    def update_data(self, data, id):
        """
        Update an existing data item.

        Args:
            data (dict): Updated data.
            id (str): Path to the JSON file.

        Returns:
            tuple: (bool, dict) Success flag and updated data.
        """
        true_false, data = self.query_file.modify_data(data, id)
        return true_false, data
    
    def delete_data(self, id, option):
        """
        Delete a data item and its dependencies if applicable.

        Args:
            id (str): Path to the JSON file.
            option (str): Entity type.

        Returns:
            tuple: (dict, int) Response message and HTTP status code.
        """
        if option == "product_registration":
            data, _ = self.get_data_item(id)
            product_id = data.get("product_id")
            inventory_id = data.get("inventory_id")
            self._delete_data(product_id, "products")
            self._delete_data(inventory_id, "inventory")
        if option == "user_registration":
            data, _ = self.get_data_item(id)
            user_id = data.get("user_id")
            self._delete_data(user_id, "users")
        if option == "carts":
            data, _ = self.get_data_item(id)
            sale_id = data.get("sale_id")
            receipt_id = data.get("receipt_id")
            self._delete_data(receipt_id, "receipts")
            self._delete_data(sale_id, "sales")
        true_false, http_code = self.query_file.delete_data(id)
        _id = id.split("/")[-1].split(".")[0]
        if true_false:
            return {"message":f"{option} ID {_id} has been deleted!"}, http_code
        return {"message":f"{option} ID {_id} was already deleted!"}, http_code

    def _delete_data(self ,id, option):
        """
        Delete a dependent data item by its ID and entity type.

        Args:
            id (str): Entity ID.
            option (str): Entity type.

        Returns:
            tuple: (dict, int) Response message and HTTP status code.
        """
        dir_path = self.directory_mapper[option]
        file_id = f"{dir_path}/{id}.json"
        true_false, http_code = self.query_file.delete_data(file_id)
        if true_false:
            return {"message":f"{option} ID {id} has been deleted!"}, http_code
        return {"message":f"{option} ID {id} was already deleted!"}, http_code