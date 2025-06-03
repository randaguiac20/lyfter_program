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
    