from flask.views import MethodView
from flask import (Flask, request, jsonify)
from validator import (UserSchema, ProductSchema, SaleSchema,
                       RoleSchema, InventorySchema, reject_fields)
from db_connector import (DataManager)
from file_manager import (FileTransactions)
from marshmallow import ValidationError
from config import (
    ROOT_DIR, DB_DIR, REGISTRATIONS_DIR,
    ROLES_DIR, USERS_DIR, INVENTORY_DIR,
    SALES_DIR, PRODUCTS_DIR,
    USERS_REGISTRATION_DIR, PRODUCT_REGISTRATION_DIR
)
from datetime import datetime
import uuid


# self.product_schema = ProductSchema()
# self.sale_schema = SaleSchema()
# self.role_schema = RoleSchema()
# self.inventory_schema = InventorySchema()

class UserRegistration(MethodView):
    def __init__(self):
        self.user_schema = UserSchema()
        self.db = DataManager()
        self.user_registration_dir = USERS_REGISTRATION_DIR

    def _get(self, user_id):
        if user_id:
            user_registration_id = f"{self.user_registration_dir}/{user_id}.json"
            data = self.db.get_registered_user(user_registration_id)
        if user_id is None:
            data = self.db.get_registered_users(self.user_registration_dir)
            filter_status = request.headers.get("status")
            data = list(
            filter(lambda _status: _status["status"] == filter_status, data)
            )
        return data

    def get(self, user_id=None):
        data = self._get(user_id)
        return jsonify(data), 200
    
    @reject_fields("status", "user_id")
    def post(self):
        request_data = request.json
        request_data['user_id'] = str(uuid.uuid4())
        request_data['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        request_data['status'] = "registered"
        try:
            _request_data = self.user_schema.load(request_data)
            file_id = request_data.get('user_id')
            user_filename = f"{self.user_registration_dir}/{file_id}.json"
            msg = self.db.save_user_registration(request_data, filepath=user_filename)
            return jsonify(msg), 200
        except ValidationError as err:
            print(f"Error: {err.messages}")
            return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    @reject_fields("status", "user_id")
    def put(self, user_id):
        request_data = request.json
        request_data['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        user_registration_id = f"{self.user_registration_dir}/{user_id}.json"
        true_false, data = self.db.update_registered_user(request_data, user_registration_id)
        if true_false is False:
            msg = f"User ID {data.get("user_id")} was not updated."
            return jsonify(msg), 404
        try:
            self.user_schema.load(data)
            msg = f"User ID {data.get("user_id")} was updated."
            return jsonify(msg), 200
        except ValidationError as err:
            print(f"Error: {err.messages}")
            return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    def delete(self, user_id):
        user_registration_id = f"{self.user_registration_dir}/{user_id}.json"
        data = self.db.delete_user(user_registration_id)
        return jsonify(msg), 200

class ProductRegistration(MethodView):
    def __init__(self):
        self.product_schema = ProductSchema()

    def _get_data(self):
        return {"message":"hello world!"}

    def get(self):
        return {"message":"Product Registration!"}
    
    def post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass
    

def register_api(app, name):
    user_registration = UserRegistration.as_view(f"user_registration")
    product_registration = ProductRegistration.as_view(f"product_registration")
    # user_login = EcommercePetsAPI.as_view(f"{name}")
    # product_inventory = EcommercePetsAPI.as_view(f"{name}")
    # sales = EcommercePetsAPI.as_view(f"{name}")

    app.add_url_rule(f"/{name}/user_registration", view_func=user_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/user_registration/<user_id>", view_func=user_registration, methods=["GET"])
    app.add_url_rule(f"/{name}/product_registration", view_func=product_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/user_registration/<user_id>", view_func=user_registration, methods=["PUT", "DELETE"])
    app.add_url_rule(f"/{name}/product_registration/<product_id>", view_func=product_registration, methods=["PUT", "DELETE"])

if __name__ == "__main__":
    app = Flask(__name__)
    file_transaction = FileTransactions()
    file_transaction.create_directories()
    register_api(app, "pet_shop")
    app.run(host="0.0.0.0", port=5001, debug=True)