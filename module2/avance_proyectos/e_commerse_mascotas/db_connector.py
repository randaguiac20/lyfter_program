from file_manager import FileTransactions

class DataManager:
    def __init__(self):
        self.file_transaction = FileTransactions()
    
    def get_registered_user(self, user_id):
        data = self.file_transaction.read_data(user_id)
        return data

    def get_registered_users(self, directory_path):
        data = self.file_transaction.load_all_json_files(directory_path)
        return data
    
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
    
    def save_user_registration(self, user_data, filepath):
        true_false = self.file_transaction.write_data(user_data, filepath)
        if true_false:
            return {"message": f"User ID {user_data.get("user_id")} already exist."}
        return {"message": f"User ID {user_data.get("user_id")} has been registered."}

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
        true_false = self.file_transaction.delete_data(user_id)
        if true_false:
            return {"message":f"User: {user_id} has been deleted!"}

    def delete_inventory_item(self):
        pass
    
    def delete_sale(self):
        pass
    
    def delete_product(self):
        pass