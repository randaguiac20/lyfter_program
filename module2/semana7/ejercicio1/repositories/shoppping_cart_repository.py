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
        self.manager = db_manager
        self.model_name = 'shopping_cart'
        self.model_class = _models.get(self.model_name)

    def _get_model(self):
        if not self.model_class:
            raise ValueError(f"Model '{self.model_name}' not found")
        return self.model_class

    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get Shoppig Cart records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related cart data
        """
        model_class = self._get_model()
        session = self.manager.sessionlocal()
        
        # If id is provided, try to get by ID
        if id:
            try:
                record_id = int(id)
                _query = session.query(model_class).filter_by(id=record_id)
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400
        else:
            _query = session.query(model_class)
        
        if with_relationships:
            _query = _query.options(joinedload(model_class.receipt),
                                    joinedload(model_class.cart_products))
        
        shopping_carts = self.manager.get(_query)
        
        # If querying by ID and no result found
        if id and not shopping_carts:
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
            if with_relationships and hasattr(shopping_cart, 'receipt') and shopping_cart.receipt:
                shopping_cart_data["receipt"] = {
                    "receipt_id": shopping_cart.receipt.id,
                    "payment_method": shopping_cart.receipt.payment_method,
                    "total_amount": shopping_cart.receipt.total_amount,
                    "created_at": str(shopping_cart.receipt.created_at),
                    "updated_at": str(shopping_cart.receipt.updated_at)
                } 
            # Include related address data if loaded
            if with_relationships and hasattr(shopping_cart, 'cart_products') and shopping_cart.cart_products:
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

    @require_jwt("administrator")
    def post(self):
        session = self.manager.sessionlocal()
        model_class = self._get_model()
        data = request.get_json()
        new_record = model_class(**data)
        record = self.manager.insert(session, new_record)
        
        if record is None:
            return jsonify({
            "error": "Shopping Cart already exists or violates database constraints",
            "message": "This user may already be registered or the data conflicts with existing records"
        }), 409
        return jsonify({
            "id": record.id,
            "cart_id": record.cart_id,
            "product_id": record.product_id,
            "quantity": record.quantity,
            "checkout": record.checkout,
            "created_at": str(record.created_at)
        })
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update Shopping Cart information (e.g., status or purchase_date).
        """
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        model_class = self._get_model()
        
        if not id:
            return jsonify({"error": "Shopping Cart ID is required"}), 400
        
        try:
            session = self.manager.sessionlocal()
            records = self.manager.get_by_id(session, model_class, id)
            record = records[0]
            if not record:
                return jsonify({"error": f"Shopping Cart ID {id} has not been found"}), 404
            
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
            updated_scp = self.manager.update(session, record)
            
            return jsonify({
                "id": updated_scp.id,
                "cart_id": updated_scp.cart_id,
                "product_id": updated_scp.product_id,
                "quantity": updated_scp.quantity,
                "checkout": updated_scp.checkout,
                "created_at": str(updated_scp.created_at)
            })
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @require_jwt("administrator")
    def delete(self, id):
        if not id:
            return jsonify({"error": "Shopping Cart ID is required"}), 400
        try:
            model_class = self._get_model()
            session = self.manager.sessionlocal()
            record = session.query(model_class).filter_by(id=id).first()
            if not record:
                raise ValueError(f"Shopping Cart ID {id} has not been found")
            self.manager.delete(session, record)
            msg = f"Shopping Cart with ID {id}  has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
