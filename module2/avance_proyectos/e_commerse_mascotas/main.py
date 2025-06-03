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
from users import UserRegistration
from products import ProductRegistration
import uuid


# self.product_schema = ProductSchema()
# self.sale_schema = SaleSchema()
# self.role_schema = RoleSchema()
# self.inventory_schema = InventorySchema()


def register_api(app, name):
    user_registration = UserRegistration.as_view(f"user_registration")
    product_registration = ProductRegistration.as_view(f"product_registration")
    # user_login = EcommercePetsAPI.as_view(f"{name}")
    # product_inventory = EcommercePetsAPI.as_view(f"{name}")
    # sales = EcommercePetsAPI.as_view(f"{name}")

    # user_registration
    app.add_url_rule(f"/{name}/user_registration", view_func=user_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/user_registration/<user_id>", view_func=user_registration, methods=["GET"])
    app.add_url_rule(f"/{name}/user_registration/<user_id>", view_func=user_registration, methods=["PUT", "DELETE"])
    
    # product_registration
    app.add_url_rule(f"/{name}/product_registration", view_func=product_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/product_registration/<product_id>", view_func=product_registration, methods=["GET"])
    app.add_url_rule(f"/{name}/product_registration/<product_id>", view_func=product_registration, methods=["PUT", "DELETE"])


if __name__ == "__main__":
    app = Flask(__name__)
    file_transaction = FileTransactions()
    file_transaction.create_directories()
    register_api(app, "pet_shop")
    app.run(host="0.0.0.0", port=5001, debug=True)