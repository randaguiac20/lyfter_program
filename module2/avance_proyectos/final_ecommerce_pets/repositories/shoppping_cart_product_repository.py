"""shoppping_cart_product_repository.py

Shopping cart product repository for managing cart item records.
Handles CRUD operations for products added to shopping carts,
including quantity and checkout status.
"""

import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt
from modules.models import _models



class ShoppingCartProductRepository(Repository):
    """
    Repository for managing shopping cart product records.
    
    Handles items added to shopping carts with relationships
    to products and carts.
    
    Attributes:
        db_manager: Database manager instance.
        model_class: The ShoppingCartProduct model class.
    """
    
    def __init__(self, db_manager, *args, **kwargs):
        """
        Initialize the shopping cart product repository.
        
        Args:
            db_manager: Database manager instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_class = _models.get('shopping_cart_product')

    def _get(self, id=None):
        """
        Internal method to retrieve shopping cart product records.
        
        Args:
            id (int, optional): Filter by cart product ID.
            
        Returns:
            tuple: (JSON response with cart product data, HTTP status code)
        """
        model_class = self.model_class
        relationship_list = [model_class.product, model_class.carts]
        session = self.db_manager.sessionlocal()
        shopping_cart_products = self.db_manager.get_query(session, model_class, id=id,
                                                           relationships=relationship_list)
        # If querying by ID and no result found
        if id and not shopping_cart_products:
            return jsonify({"error": "Shopping Cart Product not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        shopping_cart_product_list = []
        for shopping_cart_product in shopping_cart_products:
            scp_data = {
                "id": shopping_cart_product.id,
                "cart_id": shopping_cart_product.cart_id,
                "product_id": shopping_cart_product.product_id,
                "checkout": shopping_cart_product.checkout,
                "created_at": str(shopping_cart_product.created_at) if shopping_cart_product.created_at else None,
                "updated_at": str(shopping_cart_product.updated_at) if shopping_cart_product.updated_at else None
            }
            # Include related address data if loaded
            if hasattr(shopping_cart_product, 'product') and shopping_cart_product.product:
                scp_address = shopping_cart_product.product
                scp_data["product"] = {
                    "product_id": scp_address.id,
                    "name": scp_address.name,
                    "description": scp_address.description,
                    "price": scp_address.price,
                    "size": scp_address.size,
                    "quantity": scp_address.quantity
                }
            # Include related cart data if loaded
            if hasattr(shopping_cart_product, 'cart') and shopping_cart_product.cart:
                cart_list = []
                for cart in shopping_cart_product.cart:
                    cart_data = {
                        "cart_id": cart.id,
                        "user_id": cart.user_id,
                        "status": cart.status,
                        "purchase_date": cart.purchase_date,
                        "created_at": str(cart.created_at),
                        "updated_at": str(cart.updated_at)
                    }
                    cart_list.append(cart_data)
                scp_data["contacts"] = cart_list    
            shopping_cart_product_list.append(scp_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and shopping_cart_product_list:
            return jsonify(shopping_cart_product_list[0]), 200
        
        return jsonify(shopping_cart_product_list), 200

    def _add(self, data):
        """
        Internal method to create a new cart product entry.
        
        Args:
            data (dict): Cart product data with cart_id, product_id,
                        quantity, and checkout status.
            
        Returns:
            tuple: (JSON response with new cart product data, HTTP status code)
        """
        session = self.db_manager.sessionlocal()
        model_class = self.model_class

        _shopping_cart_product = model_class(**data)
        shopping_cart_product = self.db_manager.insert(session, _shopping_cart_product)
        
        if shopping_cart_product is None:
            return jsonify({
                "error": "Shopping Cart Product already exists or violates database constraints",
                "message": "This user may already be registered or the data conflicts with existing records"
            }), 409
        return jsonify({
                "id": shopping_cart_product.id,
                "cart_id": shopping_cart_product.cart_id,
                "product_id": shopping_cart_product.product_id,
                "quantity": shopping_cart_product.quantity,
                "checkout": shopping_cart_product.checkout,
                "created_at": str(shopping_cart_product.created_at)
            }), 200

    def _update(self, id, new_data):
        """
        Internal method to update a cart product entry.
        
        Args:
            id (int): Cart product ID to update.
            new_data (dict): Fields to update.
            
        Returns:
            tuple: (JSON response, HTTP status code)
        """
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400

        if not id:
            return jsonify({"error": "Shopping Cart Product ID is required"}), 400
        
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            shopping_cart_products = self.db_manager.get_query(session, model_class, id=id)
            shopping_cart_product = shopping_cart_products[0]
            if not shopping_cart_product:
                return jsonify({"error": f"Shopping Cart Product ID {id} has not been found"}), 404
            
            for column in shopping_cart_product.__table__.columns:
                field_name = column.name
                
                # Skip fields that shouldn't be updated
                if field_name in ('id', 'created_at', 'updated_at'):
                    continue
                
                # Check if field is in new_data
                if field_name in new_data:
                    old_value = getattr(shopping_cart_product, field_name)
                    new_value = new_data[field_name]
                    
                    # Compare values (handle type conversions)
                    if str(old_value) != str(new_value):
                        setattr(shopping_cart_product, field_name, new_value)
            
            if not shopping_cart_product:
                return jsonify({"error": "No fields to update"}), 400

            # Update user
            updated_scp = self.db_manager.update(session, shopping_cart_product)
            if updated_scp:
                return jsonify({
                    "id": updated_scp.id,
                    "cart_id": updated_scp.cart_id,
                    "product_id": updated_scp.product_id,
                    "quantity": updated_scp.quantity,
                    "checkout": updated_scp.checkout,
                    "created_at": str(updated_scp.created_at)
                }), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def _remove(self, id):
        """
        Internal method to delete a cart product entry.
        
        Args:
            id (int): Cart product ID to delete.
            
        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
        if not id:
            return jsonify({"error": "Shopping Cart Product ID is required"}), 400
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            shopping_cart_products = self.db_manager.get_query(session, model_class, id=id)
            shopping_cart_product = shopping_cart_products[0]
            if not shopping_cart_product:
                raise ValueError(f"Shopping Cart Product ID {id} has not been found")
            self.db_manager.delete(session, shopping_cart_product)
            msg = f"Shopping Cart Product with ID {id}  has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @require_jwt(["administrator", "client"])
    def get(self, id=None):
        """
        Get Shopping Cart Product records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related cart data
        """
        records, http_code = self._get(id=id)
        return records, http_code

    @require_jwt(["administrator", "client"])
    def post(self):
        """
        Create a new cart product entry.
        
        Requires administrator role.
        
        Returns:
            tuple: (JSON response with new cart product data, HTTP status code)
        """
        data = request.get_json()
        new_record, http_code = self._add(data)
        return new_record, http_code

    @require_jwt(["administrator", "client"])
    def put(self, id):
        """
        Update Shopping Cart Product information (e.g., quantity or checkout).
        """
        data = request.get_json()
        updated_record, http_code = self._update(id, data)
        return updated_record, http_code

    @require_jwt(["administrator", "client"])
    def delete(self, id):
        """
        Delete a cart product entry.
        
        Requires administrator role.
        
        Args:
            id (int): Cart product ID to delete.
            
        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
        deleted_record, http_code = self._remove(id)
        return deleted_record, http_code

