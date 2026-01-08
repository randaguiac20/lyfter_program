import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt



class ShoppingCartProductRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('shopping_cart_product')
        self.model_class = self.db_manager._get_model()

    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get Shopping Cart Product records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related cart data
        """
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        # If id is provided, try to get by ID
        if id:
            try:
                id = int(id)
                shopping_cart_products = self.db_manager.get_by_id(session, id)
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400
        else:
            shopping_cart_products = self.db_manager.get_query(session)
        
        if with_relationships:
            _query = session.query(model_class)
            _query_with_options = _query.options(joinedload(model_class.product),
                                                 joinedload(model_class.carts))
            shopping_cart_products = self.db_manager.get(_query_with_options)
        
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
            if with_relationships and hasattr(shopping_cart_product, 'product') and shopping_cart_product.product:
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
            if with_relationships and hasattr(shopping_cart_product, 'cart') and shopping_cart_product.cart:
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
            return jsonify(shopping_cart_product_list[0])
        
        return jsonify(shopping_cart_product_list)

    @require_jwt("administrator")
    def post(self):
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        data = request.get_json()
        new_record = model_class(**data)
        record = self.db_manager.insert(session, new_record)
        
        if record is None:
            return jsonify({
            "error": "Shopping Cart Product already exists or violates database constraints",
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
        Update Shopping Cart Product information (e.g., quantity or checkout).
        """
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        model_class = self._get_model()
        
        if not id:
            return jsonify({"error": "Shopping Cart Product ID is required"}), 400
        
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, model_class, id)
            record = records[0]
            if not record:
                return jsonify({"error": f"Shopping Cart Product ID {id} has not been found"}), 404
            
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
            updated_scp = self.db_manager.update(session, record)
            if updated_scp:
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
            return jsonify({"error": "Shopping Cart Product ID is required"}), 400
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, id)
            record = records[0]
            if not record:
                raise ValueError(f"Shopping Cart Product ID {id} has not been found")
            self.db_manager.delete(session, record)
            msg = f"Shopping Cart Product with ID {id}  has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
