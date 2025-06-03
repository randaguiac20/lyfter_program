from file_manager import FileTransactions

class DataManager:
    def __init__(self):
        self.file_transaction = FileTransactions()
    
    def get_registered_user(self, user_id):
        data = self.file_transaction.read_data(user_id)
        if data:
            return data, 200
        return data, 404

    def get_registered_users(self, directory_path):
        data = self.file_transaction.load_all_json_files(directory_path)
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
    
    def save_user_registration(self, user_data, filepath, directory_path):
        data = self.file_transaction.load_all_json_files(directory_path)
        user_exist = any(d.get("email") == user_data.get("email") or
                         d.get("name") == user_data.get("name") and
                         d.get("lastname") == user_data.get("lastname")
                         for d in data)
        if user_exist:
            return {"message": f"User email under {user_data.get("user_id")} already exist."}, 403
        true_false = self.file_transaction.write_data(user_data, filepath)
        if true_false:
            return {"message": f"User ID {user_data.get("user_id")} already exist."}, 403
        return {"message": f"User ID {user_data.get("user_id")} has been registered."}, 200

    def save_product_registration(self):
        pass
    
    def save_user(self):
        pass
    
    def save_inventory_item(self):
        pass
    
    def save_sale(self):
        pass
    
    def save_product(self):
        pass
    
    def update_registered_user(self, data, user_id):
        true_false, data = self.file_transaction.modify_data(data, user_id)
        return true_false, data
    
    def update_user(self):
        pass
    
    def update_inventory_item(self):
        pass
    
    def update_sale(self):
        pass
    
    def delete_product(self):
        pass
    
    def delete_user(self, user_id):
        true_false, http_code = self.file_transaction.delete_data(user_id)
        _user_id = user_id.split("/")[-1].split(".")[0]
        if true_false:
            return {"message":f"User: {_user_id} has been deleted!"}, http_code
        return {"message":f"User: {_user_id} was already deleted!"}, http_code

    def delete_inventory_item(self):
        pass
    
    def delete_sale(self):
        pass
    
    def delete_product(self):
        pass