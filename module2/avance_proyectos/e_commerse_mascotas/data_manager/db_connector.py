from datetime import datetime
from configurations.config import directory_mapper, admin_user, admin_role, USERS_DIR, ROLES_DIR
from data_manager.file_manager import FileTransactions,EntityDatasetManager
from validators.validator import duplicate_content_checker


class DataManager:
    def __init__(self):
        self.query_file = FileTransactions()
        self.entity_dm = EntityDatasetManager()
        self.directory_mapper = directory_mapper
    
    def create_admin_data(self):
        admin_user['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        admin_role['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        _ = self.query_file.write_data(admin_user, f"{USERS_DIR}/admin_user.json")
        _ = self.query_file.write_data(admin_role, f"{ROLES_DIR}/admin_role.json")

    def get_data_item(self, id):
        data = self.query_file.read_data(id)
        if data:
            return data, 200
        return data, 404
    
    def get_data_by_email(self, directory_path, email, admin=None):
        data, http_code = self.get_data_items(directory_path)
        user_data = [d for d in data if d.get("email") == email]
        if user_data[0].get("status") == "active":
            return user_data[0], http_code
        if user_data[0].get("status") != "active":
            return user_data, 400
        return user_data, 404

    def get_data_items(self, directory_path):
        data = self.query_file.load_all_json_files(directory_path)
        return data, 200
    
    def get_user(self, user):
        pass
    
    def get_users(self):
        pass
    
    def get_inventory_item(self):
        pass
    
    def get_inventory_items(self):
        pass
    
    def get_sale(self, sale_number):
        pass
    
    def get_sales(self):
        pass
    
    def get_product(self, product):
        pass

    def get_products(self):
        pass
            
    def save_registration_data(self, request_data, filepath, directory_path, option):
        files_data = self.query_file.load_all_json_files(directory_path)
        data_exist = duplicate_content_checker(files_data, request_data, option)
        if data_exist:
            return {"message": f"{option} ID under {request_data.get("id")} already exist."}, 403
        true_false = self.query_file.write_data(request_data, filepath)
        files_data = self.query_file.load_all_json_files(directory_path)
        if option == "product_registration":
            self.entity_dm.filter_new_entity_data(files_data, "inventory")
            inventory_id = request_data.get("inventory_id")
            self.entity_dm.create_entity("inventory", inventory_id)
            self.entity_dm.filter_new_entity_data(files_data, "product")
            product_id = request_data.get("product_id")
            self.entity_dm.create_entity("product", product_id)
        if option == "user_registration":
            self.entity_dm.filter_new_entity_data(files_data, "user")
            user_id = request_data.get("user_id")
            self.entity_dm.create_entity("user", user_id)
        if true_false:
            return {"message": f"{option} ID {request_data.get("id")} already exist."}, 403
        return {"message": f"{option} ID {request_data.get("id")} has been registered."}, 200

    def save_data(self):
        pass
    
    def save_inventory_item(self):
        pass
    
    def save_sale(self):
        pass
    
    def save_product(self):
        pass
    
    def update_registered_data(self, data, id):
        true_false, data = self.query_file.modify_data(data, id)
        return true_false, data
    
    def update_user(self):
        pass
    
    def update_inventory_item(self):
        pass
    
    def update_sale(self):
        pass
    
    def delete_data(self, id, option):
        if option == "product_registration":
            registration_data, _ = self.get_data_item(id)
            product_id = registration_data.get("product_id")
            inventory_id = registration_data.get("inventory_id")
            self.delete_product(product_id, "product")
            self.delete_inventory_item(inventory_id, "inventory")
        if option == "user_registration":
            registration_data, _ = self.get_data_item(id)
            user_id = registration_data.get("user_id")
            self.delete_user(user_id, "user")
        true_false, http_code = self.query_file.delete_data(id)
        _id = id.split("/")[-1].split(".")[0]
        if true_false:
            return {"message":f"{option} ID {_id} has been deleted!"}, http_code
        return {"message":f"{option} ID {_id} was already deleted!"}, http_code

    def delete_inventory_item(self, id, option):
        _id = f"{self.directory_mapper.get("inventory")}/{id}.json"
        true_false, http_code = self.query_file.delete_data(_id)
        if true_false:
            return {"message":f"{option} ID {_id} has been deleted from inventory!"}, http_code
        return {"message":f"{option} ID {_id} was already deleted!"}, http_code
    
    def delete_product(self, id, option):
        _id = f"{self.directory_mapper.get("product")}/{id}.json"
        true_false, http_code = self.query_file.delete_data(_id)
        if true_false:
            return {"message":f"{option} ID {_id} has been deleted!"}, http_code
        return {"message":f"{option} ID {_id} was already deleted from products!"}, http_code
    
    def delete_user(self, id, option):
        _id = f"{self.directory_mapper.get("user")}/{id}.json"
        true_false, http_code = self.query_file.delete_data(_id)
        if true_false:
            return {"message":f"{option} ID {_id} has been deleted!"}, http_code
        return {"message":f"{option} ID {_id} was already deleted from products!"}, http_code
    
    def delete_sale(self):
        pass