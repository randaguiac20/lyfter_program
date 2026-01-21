"""buy_fruits_repository.py

Public API repository for customer fruit purchases.
Orchestrates the creation of shopping carts, cart products, and receipts
for customer purchase transactions.
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



def get_email_from_token(jwt_manager, _token):
    """
    Extract email address from JWT token.
    
    Args:
        jwt_manager: JWT manager instance for decoding.
        _token (str): Authorization header value with Bearer prefix.
        
    Returns:
        str: Email address from decoded token, or error response.
    """
    token = _token.replace("Bearer ","")
    if not token:
        return jsonify({"error": "No token provided"}), 400
    
    decoded = jwt_manager.decode(token)
    email = decoded.get("email")
    return email

def get_records(model=None, email=None, id=None, name=None):
    """
    Generic record retrieval helper function.
    
    Args:
        model: Repository instance to query.
        email (str, optional): Filter by email.
        id (int, optional): Filter by ID.
        name (str, optional): Filter by name.
        
    Returns:
        Query results from the model's _get method.
    """
    if email:
        records = model._get(email=email)
    elif id:
        records = model._get(id=id)
    elif name:
        records = model._get(name=name)
    else:
        records = model._get()
    return records

def get_product(data=None, model=None):
    """
    Validate products exist and have sufficient stock.
    
    Args:
        data (list): List of product dictionaries with name and quantity.
        model: Product repository instance.
        
    Returns:
        tuple: (None, 200) if valid, (error response, error code) if invalid.
    """
    for record in data:
        name = record["name"]
        products = get_records(model=model, name=name)
        product = products[0]
        # 1. Validate product exist in the stock
        if not product:
            return jsonify({"error": "No product record found"}), 404
        
        # 2. Validate stock for the product
        product_quantity = product.get_json()[0].get("quantity")
        if product_quantity <= 0 or record["quantity"] > product_quantity:
            return jsonify({"error": f"No product available in the stock, current amount {product_quantity}"}), 400
        if record["quantity"] > product_quantity:
            return jsonify({"error": f"Insuficient product in the stock, current amount {product_quantity}"}), 400
    return None, 200

def add_cart(model=None, user_id=None):
    """
    Create a new shopping cart for a user.
    
    Args:
        model: Shopping cart repository instance.
        user_id (int): User ID to associate with the cart.
        
    Returns:
        tuple: (cart data dict, HTTP status code)
    """
    sc_cart_data = {
            "user_id": user_id,
        }
    response, http_code = model._add(sc_cart_data)
    if http_code != 200:
        return response, http_code
    # Extract cart data from JSON response - already formatted correctly
    cart = response.get_json()
    return cart, 200

def validate_products(data=None):
    """
    Validate product data against schema requirements.
    
    Args:
        data (list): List of product dictionaries to validate.
        
    Returns:
        tuple: (validated data, message) or (False, error message)
    """
    for record in data:
        _new_record, msg = validate_buy_fruits(record)
        if _new_record is False:
            return jsonify({
                "error": msg
            }), 400
    return _new_record, msg

def get_product_details(model=None, name=None, size=None):
    """
    Get product_id and price from product name and size.
    
    Args:
        model: Product repository instance.
        name (str): Product name to search for.
        size (str): Product size to match.
        
    Returns:
        tuple: (product_id, price) or (None, None) if not found.
    """
    response, http_code = model._get(name=name)
    if http_code != 200:
        return None, None
    products = response.get_json()
    for product in products:
        if product.get("size") == size:
            return product.get("id"), product.get("price")
    return None, None

def add_cart_product(model=None, cart_id=None, product_id=None, quantity=None):
    """
    Create a shopping cart product entry.
    
    Args:
        model: Shopping cart product repository instance.
        cart_id (int): Cart ID to associate with.
        product_id (int): Product ID to add.
        quantity (int): Quantity of the product.
        
    Returns:
        tuple: (cart product data dict, HTTP status code)
    """
    cart_product_data = {
        "cart_id": cart_id,
        "product_id": product_id,
        "quantity": quantity,
        "checkout": False
    }
    response, http_code = model._add(cart_product_data)
    if http_code != 200:
        return response, http_code
    cart_product = response.get_json()
    return cart_product, 200

def add_receipt(model=None, cart_id=None, payment_method="cash", total_amount=0):
    """
    Create a receipt for the shopping cart.
    
    Args:
        model: Receipt repository instance.
        cart_id (int): Cart ID to associate with.
        payment_method (str): Payment method (default: 'cash').
        total_amount (float): Total purchase amount.
        
    Returns:
        tuple: (receipt data dict, HTTP status code)
    """
    receipt_data = {
        "cart_id": cart_id,
        "payment_method": payment_method,
        "total_amount": total_amount
    }
    response, http_code = model._add(receipt_data)
    if http_code != 200:
        return response, http_code
    receipt = response.get_json()
    return receipt, 200


class BuyFruitRepository(Repository):
    """
    Repository for managing fruit purchase transactions.
    
    Orchestrates the complete purchase workflow: creating shopping carts,
    adding products to carts, and generating receipts.
    
    Attributes:
        jwt_manager: JWT manager for token validation.
        shopping_cart: Shopping cart repository instance.
        receipt: Receipt repository instance.
        registration: Registration repository instance.
        user: User repository instance.
        product: Product repository instance.
        cart_product: Shopping cart product repository instance.
    """
    
    def __init__(self, db_manager):
        """
        Initialize the buy fruit repository.
        
        Args:
            db_manager: Database manager instance.
        """
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__()
        self.jwt_manager = JWT_Manager()
        self.shopping_cart = ShoppingCartRepository(db_manager)
        self.receipt = ReceiptRepository(db_manager)
        self.registration = RegistrationRepository(db_manager)
        self.user = UserRepository(db_manager)
        self.product = ProductRepository(db_manager)
        self.cart_product = ShoppingCartProductRepository(db_manager)

    @require_jwt(["administrator", "client"])
    def get(self, id=None):
        """
        Get Fruit purchase records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
        """
        # Get email from token
        _token = request.headers.get("Authorization")
        email = get_email_from_token(self.jwt_manager, _token)

        email_records = get_records(model=self.registration, email=email)
        email_record = email_records[0]
        if not email_record:
            return jsonify({"error": f"No record found for {email}"}), 404
        
        # Matched user gotten from token
        users = get_records(model=self.user)
        if not users:
            return jsonify({"error": "No users records found"}), 404
        
        user_id = None
        for user in users:
            if email_record.id == user.registration_id:
                user_id = user.id
        # If id is provided, try to get by ID
        if id:
            receipts = get_records(model=self.receipt, id=id)
        else:
            receipts = get_records(model=self.receipt)
        # If querying by ID and no result found
        if id and not receipts:
            return jsonify({"error": "Receipt was not found"}), 404

        # Convert SQLAlchemy objects to dictionaries
        receipt_list = []
        cart_list = []
        #receipt_list = get_receipts(receipts)
        for receipt in receipts:
            receipt_data = {
                "id": receipt.id,
                "cart_id": receipt.cart_id,
                "payment_method": receipt.payment_method,
                "created_at": str(receipt.created_at) if receipt.created_at else None,
                "updated_at": str(receipt.updated_at) if receipt.updated_at else None
            }
            # Include related address data if loaded
            carts = get_records(model=self.shopping_cart, id=receipt.cart_id)
            cart = carts[0]
            if cart.id == receipt.cart_id and cart.user_id == user_id:
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
        """
        Process a fruit purchase transaction.
        
        Creates a shopping cart, adds cart products for each item,
        and generates a receipt with the total amount.
        
        Requires administrator or client role.
        
        Returns:
            tuple: (JSON response with cart, products, receipt, HTTP 201)
        """
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "JSON Data is not correct, provide a list of items."}), 400
        # Get email from token
        _token = request.headers.get("Authorization")
        email = get_email_from_token(self.jwt_manager, _token)
        
        email_records = get_records(model=self.registration, email=email)
        email_record = email_records[0]
        if not email_record:
            return jsonify({"error": f"No record found for {email}"}), 404
        email_registration_id = email_record.get_json()[0].get("registration_id")
        _, _ = validate_products(data)

        # Matched user gotten from token      
        users, _ = get_records(model=self.user)
        
        if not users:
            return jsonify({"error": "No users records found"}), 404
        
        user_id = None
        users = users.get_json()
        for user in users:
            user_registration_id = user.get("registration_id")
            if email_registration_id == user_registration_id:
                user_id = user.get("id")

        # Validate the product exist and matches
        _, _ = get_product(data=data, model=self.product)
        
        # Create shopping cart
        cart_data, http_code = add_cart(model=self.shopping_cart, user_id=user_id)
        if http_code != 200:
            return cart_data, http_code
        
        cart_id = cart_data.get("id")
        total_amount = 0
        cart_products_list = []
        
        # Create cart products for each item in the order
        for item in data:
            product_id, price = get_product_details(
                model=self.product, 
                name=item["name"], 
                size=item["size"]
            )
            if product_id is None:
                return jsonify({"error": f"Product '{item['name']}' with size '{item['size']}' not found"}), 404
            
            # Calculate item total and add to total_amount
            item_total = price * item["quantity"]
            total_amount += item_total
            
            # Create cart product
            cart_product_data, http_code = add_cart_product(
                model=self.cart_product,
                cart_id=cart_id,
                product_id=product_id,
                quantity=item["quantity"]
            )
            if http_code != 200:
                return cart_product_data, http_code
            cart_products_list.append(cart_product_data)
        
        # Create receipt
        receipt_data, http_code = add_receipt(
            model=self.receipt,
            cart_id=cart_id,
            payment_method="cash",
            total_amount=total_amount
        )
        if http_code != 200:
            return receipt_data, http_code
        
        # Build complete response
        response_data = {
            "cart": cart_data,
            "cart_products": cart_products_list,
            "receipt": receipt_data
        }
        
        return jsonify(response_data), 201
    
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
        """
        Delete a fruit purchase record.
        
        Requires administrator role.
        
        Args:
            id (int): Purchase record ID to delete.
            
        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
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
