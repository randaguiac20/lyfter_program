import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt



class ReceiptRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('receipt')
        self.model_class = self.db_manager._get_model()

    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get Receipt records.
        
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
                receipts = self.db_manager.get_by_id(session, id)
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400
        else:
            receipts = self.db_manager.get_query(session)
        
        if with_relationships:
            _query = session.query(model_class)
            _query_with_options = _query.options(joinedload(model_class.cart))
            receipts = self.db_manager.get_query(_query_with_options)
        
        # If querying by ID and no result found
        if id and not receipts:
            return jsonify({"error": "Receipt not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        receipts_list = []
        for receipt in receipts:
            receipt_data = {
                "id": receipt.id,
                "cart_id": receipt.cart_id,
                "payment_method": receipt.payment_method,
                "total_amount": receipt.total_amount,
                "created_at": str(receipt.created_at) if receipt.created_at else None,
                "updated_at": str(receipt.updated_at) if receipt.updated_at else None
            }
            # Include related cart data if loaded
            if with_relationships and hasattr(receipt, 'cart') and receipt.cart:
                receipt_data["receipt"] = {
                    "cart_id": receipt.cart.cart_id,
                    "product_id": receipt.cart.product_id,
                    "quantity": receipt.cart.quantity,
                    "checkout": receipt.cart.checkout,
                    "created_at": str(receipt.cart.created_at),
                    "updated_at": str(receipt.cart.updated_at)
                }

            receipts_list.append(receipt_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and receipts_list:
            return jsonify(receipts_list[0])
        
        return jsonify(receipts_list)

    @require_jwt("administrator")
    def post(self):
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        data = request.get_json()
        new_record = model_class(**data)
        record = self.db_manager.insert(session, new_record)
        
        if record is None:
            return jsonify({
            "error": "Receipt already exists or violates database constraints",
            "message": "This user may already be registered or the data conflicts with existing records"
        }), 409
        return jsonify({
            "id": record.id,
            "cart_id": record.cart_id,
            "payment_method": record.payment_method,
            "total_amount": record.total_amount,
            "created_at": str(record.created_at)
        })
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update Receipt information (e.g., status or purchase_date).
        """
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        
        if not id:
            return jsonify({"error": "Receipt ID is required"}), 400
        
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, id)
            record = records[0]
            if not record:
                return jsonify({"error": f"Receipt ID {id} has not been found"}), 404
            
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
            updated_receipt = self.db_manager.update(session, record)
            
            return jsonify({
                "id": updated_receipt.id,
                "cart_id": updated_receipt.cart_id,
                "payment_method": updated_receipt.payment_method,
                "total_amount": updated_receipt.total_amount,
                "created_at": str(updated_receipt.created_at)
            })
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @require_jwt("administrator")
    def delete(self, id):
        if not id:
            return jsonify({"error": "Receipt ID is required"}), 400
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, id)
            record = records[0]
            if not record:
                raise ValueError(f"Receipt ID {id} has not been found")
            self.db_manager.delete(session, record)
            msg = f"Receipt with ID {id}  has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
