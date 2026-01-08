import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt



class ProductRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('product')
        self.model_class = self.db_manager._get_model()

    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get product records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related product data
        """
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        # If id is provided, try to get by ID
        if id:
            try:
                id = int(id)
                products = self.db_manager.get_by_id(session, id)
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400
        else:
            products = self.db_manager.get_query(session)
        
        if with_relationships:
            _query = session.query(model_class)
            _query_with_options = _query.options(joinedload(model_class.cart_products))
            products = self.db_manager.get(_query_with_options)
        
        # If querying by ID and no result found
        if id and not products:
            return jsonify({"error": "product not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        product_list = []
        for product in products:
            product_data = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "size": product.size,
                "quantity": product.quantity,
                "created_at": str(product.created_at) if product.created_at else None,
                "updated_at": str(product.updated_at) if product.updated_at else None
            }
            # Include related address data if loaded
            if with_relationships and hasattr(product, 'cart_products') and product.cart_products:
                cart_list = []
                for cart_product in product.cart_products:
                    cart_data = {
                        "cart_id": cart_product.cart_id,
                        "product_id": cart_product.product_id,
                        "quantity": cart_product.quantity,
                        "checkout": cart_product.checkout,
                        "created_at": str(cart_product.created_at),
                        "updated_at": str(cart_product.updated_at)
                    }
                    cart_list.append(cart_data)
                product_data['cart_prodcuts'] = cart_list
            product_list.append(product_data)         

        # Return single object if querying by ID, otherwise return list
        if id and product_list:
            return jsonify(product_list[0])
        
        return jsonify(product_list)

    @require_jwt("administrator")
    def post(self):
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "JSON Data is not correct, provide a list of items."}), 400
        record_list = []
        for record in data:
            _new_record = model_class(**record)
            new_record = self.db_manager.insert(session, _new_record)

            if new_record is None:
                return jsonify({
                "error": "Product already exists or violates database constraints",
                "message": "This user may already be registered or the data conflicts with existing records"
            }), 409
            record["created_at"] = new_record.created_at
            record_list.append(record)
        return jsonify(record_list)

    @require_jwt("administrator")
    def put(self, id):
        """
        Update product information (e.g., name, size or quantity).
        """
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        
        if not id:
            return jsonify({"error": "Product ID is required"}), 400
        
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, id)
            record = records[0]
            if not record:
                return jsonify({"error": f"Product ID {id} has not been found"}), 404
            
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

            # Update product
            updated_product = self.db_manager.update(session, record)
            
            return jsonify({
                "id": updated_product.id,
                "name": updated_product.name,
                "price": updated_product.price,
                "quantity": updated_product.quantity,
                "size": updated_product.size,
                "updated_at": str(updated_product.updated_at)
            })
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @require_jwt("administrator")
    def delete(self, id):
        if not id:
            return jsonify({"error": "Product ID is required"}), 400
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, id)
            record = records[0]
            if not record:
                raise ValueError(f"Product ID {id} has not been found")
            self.db_manager.delete(session, record)
            msg = f"Product with ID {id} with name {record.name} has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
