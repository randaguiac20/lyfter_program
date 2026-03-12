"""shoppping_cart_repository.py

Shopping cart repository for managing customer cart records.
Handles CRUD operations for shopping carts with status tracking
and relationships to products and receipts.
"""

import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.jwt_manager import require_jwt
from modules.models import _models


class ShoppingCartRepository(Repository):
    """
    Repository for managing shopping cart records.
    
    Handles cart creation, status updates, and relationships
    to cart products and receipts.
    
    Attributes:
        db_manager: Database manager instance.
        model_class: The ShoppingCart model class.
    """
    
    def __init__(self, db_manager, *args, **kwargs):
        """
        Initialize the shopping cart repository.
        
        Args:
            db_manager: Database manager instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_class = _models.get('shopping_cart')

    def _get(self, id=None):
        """
        Internal method to retrieve shopping cart records with relationships.
        
        Args:
            id (int, optional): Filter by cart ID.
            
        Returns:
            tuple: (JSON response with cart data, HTTP status code)
        """
        model_class = self.model_class
        relationship_list= [model_class.receipt, model_class.cart_products]
        session = self.db_manager.sessionlocal()
        shopping_carts = self.db_manager.get_query(session, model_class, id=id,
                                                   relationships=relationship_list)
        
        # If querying by ID and no result found
        if shopping_carts is None:
            return jsonify({"error": "Shopping Cart not found"}), 404
        # Convert SQLAlchemy objects to dictionaries
        shopping_cart_list = []
        for shopping_cart in shopping_carts:
            shopping_cart_data = {
                "id": shopping_cart.id,
                "user_id": shopping_cart.user_id,
                "status": shopping_cart.status.value if hasattr(shopping_cart.status, 'value') else shopping_cart.status,
                "purchase_date": shopping_cart.purchase_date,
                "created_at": str(shopping_cart.created_at) if shopping_cart.created_at else None,
                "updated_at": str(shopping_cart.updated_at) if shopping_cart.updated_at else None
            }
            # Include related cart data if loaded
            if hasattr(shopping_cart, 'receipt') and shopping_cart.receipt:
                shopping_cart_data["receipt"] = {
                    "receipt_id": shopping_cart.receipt.id,
                    "payment_method": shopping_cart.receipt.payment_method,
                    "total_amount": shopping_cart.receipt.total_amount,
                    "created_at": str(shopping_cart.receipt.created_at),
                    "updated_at": str(shopping_cart.receipt.updated_at)
                } 
            # Include related address data if loaded
            if hasattr(shopping_cart, 'cart_products') and shopping_cart.cart_products:
                sc_cart_products = shopping_cart.cart_products
                shopping_cart_product_list = []
                for sc_cart_product in sc_cart_products:
                    sp_cart_product_data = {
                        "cart_id": sc_cart_product.cart_id,
                        "product_id": sc_cart_product.product_id,
                        "quantity": sc_cart_product.quantity,
                        "created_at": str(sc_cart_product.created_at),
                        "updated_at": str(sc_cart_product.updated_at)
                    }
                    shopping_cart_product_list.append(sp_cart_product_data)
                shopping_cart_data["shopping_cart_products"] = shopping_cart_product_list
             
            shopping_cart_list.append(shopping_cart_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and shopping_cart_list:
            return jsonify(shopping_cart_list[0])
        
        return jsonify(shopping_cart_list)

    def _add(self, data):
        """
        Internal method to create a new shopping cart.
        
        Args:
            data (dict): Cart data with user_id, status, and purchase_date.
            
        Returns:
            tuple: (JSON response with new cart data, HTTP status code)
        """
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        _shooping_cart = model_class(**data)
        shooping_cart = self.db_manager.insert(session, _shooping_cart)
        if shooping_cart is None:
            return jsonify({
            "error": "Shopping Cart already exists or violates database constraints",
            "message": "This user may already be registered or the data conflicts with existing records"
        }), 409
        return jsonify({
            "id": shooping_cart.id,
            "user_id": shooping_cart.user_id,
            "status": shooping_cart.status.value if hasattr(shooping_cart.status, 'value') else shooping_cart.status,
            "purchase_date": shooping_cart.purchase_date,
            "created_at": str(shooping_cart.created_at)
        }), 200

    def _update(self, id, new_data):
        """
        Internal method to update a shopping cart.
        
        Args:
            id (int): Cart ID to update.
            new_data (dict): Fields to update.
            
        Returns:
            tuple: (JSON response, HTTP status code)
        """
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        if not id:
            return jsonify({"error": "Shopping Cart ID is required"}), 400
        
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            shooping_carts = self.db_manager.get_query(session, model_class, id=id)
            shooping_cart = shooping_carts[0]
            if not shooping_cart:
                return jsonify({"error": f"Shopping Cart ID {id} has not been found"}), 404
            
            for column in shooping_cart.__table__.columns:
                field_name = column.name
                
                # Skip fields that shouldn't be updated
                if field_name in ('id', 'created_at', 'updated_at'):
                    continue
                
                # Check if field is in new_data
                if field_name in new_data:
                    old_value = getattr(shooping_cart, field_name)
                    new_value = new_data[field_name]
                    
                    # Compare values (handle type conversions)
                    if str(old_value) != str(new_value):
                        setattr(shooping_cart, field_name, new_value)
            
            if not shooping_cart:
                return jsonify({"error": "No fields to update"}), 400

            # Update user
            updated_scp = self.db_manager.update(session, shooping_cart)
            
            return jsonify({
                "id": updated_scp.id,
                "user_id": updated_scp.user_id,
                "status": updated_scp.status.value if hasattr(updated_scp.status, 'value') else updated_scp.status,
                "purchase_date": updated_scp.purchase_date,
                "updated_at": str(updated_scp.updated_at)
            }), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def _remove(self, id):
        """
        Internal method to delete a shopping cart.
        
        Args:
            id (int): Cart ID to delete.
            
        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
        if not id:
            return jsonify({"error": "Shopping Cart ID is required"}), 400
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            shooping_carts = self.db_manager.get_query(session, model_class, id=id)
            shooping_cart = shooping_carts[0]
            if not shooping_cart:
                raise ValueError(f"Shopping Cart ID {id} has not been found")
            self.db_manager.delete(session, shooping_cart)
            msg = f"Shopping Cart with ID {id}  has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @require_jwt(["administrator", "client"])
    def get(self, id=None, relationships=True):
        """
        Get Shoppig Cart records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related cart data
        """
        result = self._get(id=id)
        # Handle both tuple returns and single Response returns
        if isinstance(result, tuple):
            return result
        return result, 200

    @require_jwt(["administrator", "client"])
    def post(self):
        """
        Create a new shopping cart.

        Requires administrator or client role.

        Returns:
            tuple: (JSON response with new cart data, HTTP status code)
        """
        data = request.get_json()
        new_record, http_code = self._add(data)
        return new_record, http_code

    @require_jwt(["administrator", "client"])
    def put(self, id):
        """
        Update Shopping Cart information (e.g., status or purchase_date).
        """
        data = request.get_json()
        updated_record, http_code = self._update(id, data)
        return updated_record, http_code

    @require_jwt(["administrator", "client"])
    def delete(self, id):
        """
        Delete a shopping cart.
        
        Requires administrator role.
        
        Args:
            id (int): Cart ID to delete.
            
        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
        deleted_record, http_code = self._remove(id)
        return deleted_record, http_code
