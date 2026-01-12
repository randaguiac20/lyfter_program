import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt



class ShoppingCartRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('shopping_cart')
        self.model_class = self.db_manager._get_model()

    def _get(self, id=None, with_relationships=True):
        model_class = self.model_class
        relationship_list= [model_class.receipt, model_class.cart_products]
        session = self.db_manager.sessionlocal()
        shopping_carts = self.db_manager.get_query(session, id=id,
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
                "status": shopping_cart.status,
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
            "status": shooping_cart.status,
            "purchase_date": shooping_cart.purchase_date,
            "created_at": str(shooping_cart.created_at)
        })

    def _update(self, id, new_data):
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        if not id:
            return jsonify({"error": "Shopping Cart ID is required"}), 400
        
        try:
            session = self.db_manager.sessionlocal()
            shooping_carts = self.db_manager.get_query(session, id=id)
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
        if not id:
            return jsonify({"error": "Shopping Cart ID is required"}), 400
        try:
            session = self.db_manager.sessionlocal()
            shooping_carts = self.db_manager.get_query(session, id=id)
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
        shopping_carts, http_code = self._get(id=id,
                                              with_relationships=relationships)
        return shopping_carts, http_code

    @require_jwt(["administrator", "client"])
    def post(self, data):
        new_record, http_code = self._add(data)
        return new_record, http_code

    @require_jwt("administrator")
    def put(self, id, data):
        """
        Update Shopping Cart information (e.g., status or purchase_date).
        """
        updated_record, http_code = self._update(id, data)
        return updated_record, http_code

    @require_jwt("administrator")
    def delete(self, id):
        deleted_record, http_code = self._remove(id)
        return deleted_record, http_code
