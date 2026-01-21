"""3_buy_fruits_repository.py

DEPRECATED: This is an older version of the buy_fruits_repository.
Please use buy_fruits_repository.py instead.

This file is kept for reference purposes only.
"""

import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from repositories.login_repository import LoginRepository
from repositories.product_repository import ProductRepository
from repositories.address_repository import AddressRepository
from repositories.shoppping_cart_repository import ShoppingCartRepository
from repositories.receipt_repository import ReceiptRepository
from repositories.shoppping_cart_product_repository import ShoppingCartProductRepository
from repositories.user_repository import UserRepository
from repositories.registration_repository import RegistrationRepository
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt, JWT_Manager
from modules.db_manager import DBManager
from modules.models import validate_buy_fruits



class BuyFruitRepository(Repository):
    def __init__(self, db_manager):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__()
        self.jwt_manager = JWT_Manager()
        self.shopping_cart = ShoppingCartRepository()
        self.receipt = ReceiptRepository()
        self.registration = RegistrationRepository()
        self.user = UserRepository()
        self.product = ProductRepository()

    @require_jwt(["administrator", "client"])
    def get(self, with_relationships=True):
        """
        Get Fruit purchase records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
        """
        db_manager = self.db_manager
        session = db_manager.get_session()
        
        _token = request.headers.get("Authorization")
        token = _token.replace("Bearer ","")
        if not token:
            return jsonify({"error": "No token provided"}), 400
        
        decoded = self.jwt_manager.decode(token)
        email = decoded.get("email")

        db_manager._get_model_name("register_user")
        db_manager._get_model()

        email_records = db_manager.get_by_email(session, email)
        email_record = email_records[0]
        if not email_record:
            return jsonify({"error": f"No record found for {email}"}), 404
        
        # Matched user gotten from token
        db_manager._get_model_name("user")
        db_manager._get_model()

        users = db_manager.get_query(session)
        if not users:
            return jsonify({"error": "No users records found"}), 404
        
        user_id = None
        for user in users:
            if email_record.id == user.registration_id:
                user_id = user.id
        # If id is provided, try to get by ID
        db_manager._get_model_name("receipt")
        receipt_model_class = db_manager._get_model()

        if id:
            try:
                id = int(id)
                receipts = db_manager.get_by_id(session, id)
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400
        else:
            receipts = db_manager.get_query(session)

        if with_relationships:
            _query = session.query(receipt_model_class)
            _query_with_options = _query.options(joinedload(receipt_model_class.cart))
            receipts = db_manager.get_query(_query_with_options)
        # If querying by ID and no result found
        if id and not receipts:
            return jsonify({"error": "Receipt was not found"}), 404

        # Convert SQLAlchemy objects to dictionaries
        receipt_list = []
        for receipt in receipts:
            receipt_data = {
                "id": receipt.id,
                "cart_id": receipt.cart_id,
                "payment_method": receipt.payment_method,
                "created_at": str(receipt.created_at) if receipt.created_at else None,
                "updated_at": str(receipt.updated_at) if receipt.updated_at else None
            }
            # Include related address data if loaded

            db_manager._get_model_name("shopping_cart")
            sc_model_class = db_manager._get_model()

            if with_relationships and hasattr(receipt, 'cart') and receipt.cart:
                cart_list = []
                _query = session.query(sc_model_class)
                _query_with_options = _query.options(joinedload(sc_model_class.user))
                carts = db_manager.get_query(_query_with_options)
                for cart in carts:
                    if cart.id == receipt.id and cart.user_id == user_id:
                        cart_data = {
                            "id": cart.id,
                            "user_id": cart.user_id,
                            "status": cart.status,
                            "purchase_date": cart.purchase_date,
                            "created_at": str(cart.created_at) if cart.created_at else None,
                            "updated_at": str(cart.updated_at) if cart.updated_at else None
                        }
                        cart_list.append(cart_data)
                    receipt_data["carts"] = cart_list
            
            receipt_list.append(receipt_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and receipt_list:
            return jsonify(receipt_list[0])
        
        return jsonify(receipt_list)

    @require_jwt(["administrator", "client"])
    def post(self):
        
        db_manager = self.db_manager
        session = db_manager.get_session()

        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "JSON Data is not correct, provide a list of items."}), 400
        _token = request.headers.get("Authorization")
        token = _token.replace("Bearer ","")
        if not token:
            return jsonify({"error": "No token provided"}), 400
        decoded = self.jwt_manager.decode(token)
        email = decoded.get("email")

        db_manager._get_model_name("register_user")
        db_manager._get_model()

        email_records = db_manager.get_by_email(session, email)
        email_record = email_records[0]
        if not email_record:
            return jsonify({"error": f"No record found for {email}"}), 404
        
        for record in data:
            _new_record, msg = validate_buy_fruits(record)
            if _new_record is False:
                return jsonify({
                    "error": msg
                }), 400
        
         # Matched user gotten from token
        db_manager._get_model_name("user")
        db_manager._get_model()
        
        users = db_manager.get_query(session)
        if not users:
            return jsonify({"error": "No users records found"}), 404
        
        user_id = None
        for user in users:
            if email_record.id == user.registration_id:
                user_id = user.id
        
        # Add logic to get add/substract quantity from products based on the purchase
        # 1. Validate the product exist and matches
        db_manager._get_model_name("product")
        db_manager._get_model()
        
        record_list = []
        for record in data:

            products = db_manager.get_by_name(session, record["name"])
            product = products[0]

            # 1. Validate product exist in the stock
            if not product:
                return jsonify({"error": "No product record found"}), 404
            
            # 2. Validate stock for the product
            if product.quantity <= 0 or record["quantity"] > product.quantity:
                return jsonify({"error": f"No product available in the stock, current amount {product.quantity}"}), 400
            if record["quantity"] > product.quantity:
                return jsonify({"error": f"Insuficient product in the stock, current amount {product.quantity}"}), 400

        # 3. Create shooping cart
        db_manager._get_model_name("shopping_cart")
        sc_model_class = db_manager._get_model()

        sc_cart = {
            "user_id": user_id,
        }
        _new_record = sc_model_class(**sc_cart)
        new_record = db_manager.insert(session, _new_record)
        if new_record is None:
            return jsonify({
                "error": "Shooping cart already exists or violates database constraints",
                "message": "This Shooping cart may already be registered or the data conflicts with existing records"
            }), 409
        # Create dictionary for the response
        cart_data = {
            "id": new_record.id,
            "user_id": new_record.user_id,
            "status": new_record.status.value,
            "purchase_date": str(new_record.purchase_date) if new_record.purchase_date else None,
            "created_at": str(new_record.created_at) if new_record.created_at else None
        }
        record_list.append(cart_data)
        return jsonify(record_list)
    
    @require_jwt(["administrator", "client"])
    def put(self, id):
        """
        Update Fruit purchase information (e.g., product or quantity).
        """
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        model_class = self._get_model()
        
        if not id:
            return jsonify({"error": "Fruit purchase ID is required"}), 400
        
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, model_class, id)
            record = records[0]
            if not record:
                return jsonify({"error": f"Fruit purchase ID {id} has not been found"}), 404
            
            for column in record.__table__.columns:
                field_name = column.name
                
                # Skip fields that shouldn't be updated
                if field_name in ('id', 'created_at', 'updated_at'):
                    continue
                
                # Check if field is in new_data
                if field_name in new_data:
                    old_value = getattr(record, field_name)
                    new_value = new_data[field_name]
                    
                    # Compare values (handle type conversions)
                    if str(old_value) != str(new_value):
                        setattr(record, field_name, new_value)
            
            if not record:
                return jsonify({"error": "No fields to update"}), 400

            # Update user
            updated_user = self.db_manager.update(session, record)
            
            return jsonify({
                "id": updated_user.id,
                "user_name": f"{updated_user.first_name} {updated_user.last_name}",
                "updated_at": str(updated_user.updated_at)
            })
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @require_jwt("administrator")
    def delete(self, id):
        if not id:
            return jsonify({"error": "Fruit purchase ID is required"}), 400
        try:
            model_class = self._get_model()
            session = self.db_manager.sessionlocal()
            record = session.query(model_class).filter_by(id=id).first()
            if not record:
                raise ValueError(f"Fruit purchase ID {id} has not been found")
            self.db_manager.delete(session, record)
            msg = f"Fruit purchase with ID {id} has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
