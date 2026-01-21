import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.jwt_manager import require_jwt
from modules.models import _models



class ReceiptRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_class = _models.get('receipt')

    def _get(self, id=None):
        model_class = self.model_class
        relationship_list = [model_class.cart]
        session = self.db_manager.sessionlocal()
        receipts = self.db_manager.get_query(session, model_class, id=id,
                                             relationships=relationship_list)

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
            if hasattr(receipt, 'cart') and receipt.cart:
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
            return jsonify(receipts_list[0]), 200
        
        return jsonify(receipts_list), 200

    def _add(self, data):
        session = self.db_manager.sessionlocal()
        model_class = self.model_class

        _receipt = model_class(**data)
        receipt = self.db_manager.insert(session, _receipt)

        if receipt is None:
            return jsonify({
            "error": "Receipt already exists or violates database constraints",
            "message": "This user may already be registered or the data conflicts with existing records"
        }), 409
        return jsonify({
            "id": receipt.id,
            "cart_id": receipt.cart_id,
            "payment_method": receipt.payment_method,
            "total_amount": receipt.total_amount,
            "created_at": str(receipt.created_at)
        }), 200

    def _update(self, id, new_data):
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        
        if not id:
            return jsonify({"error": "Receipt ID is required"}), 400
        
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            receipts = self.db_manager.get_query(session, model_class, id=id)
            receipt = receipts[0]
            if not receipt:
                return jsonify({"error": f"Receipt ID {id} has not been found"}), 404
            
            for column in receipt.__table__.columns:
                field_name = column.name
                
                # Skip fields that shouldn't be updated
                if field_name in ('id', 'created_at', 'updated_at'):
                    continue
                
                # Check if field is in new_data
                if field_name in new_data:
                    old_value = getattr(receipt, field_name)
                    new_value = new_data[field_name]
                    
                    # Compare values (handle type conversions)
                    if str(old_value) != str(new_value):
                        setattr(receipt, field_name, new_value)
            
            if not receipt:
                return jsonify({"error": "No fields to update"}), 400

            # Update user
            updated_receipt = self.db_manager.update(session, receipt)
            
            return jsonify({
                "id": updated_receipt.id,
                "cart_id": updated_receipt.cart_id,
                "payment_method": updated_receipt.payment_method,
                "total_amount": updated_receipt.total_amount,
                "created_at": str(updated_receipt.created_at)
            }), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def _remove(self, id):
        if not id:
            return jsonify({"error": "Receipt ID is required"}), 400
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            receipts = self.db_manager.get_query(session, model_class, id=id)
            receipt = receipts[0]
            if not receipt:
                raise ValueError(f"Receipt ID {id} has not been found")
            self.db_manager.delete(session, receipt)
            msg = f"Receipt with ID {id}  has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @require_jwt("administrator")
    def get(self, id=None, relationships=True):
        """
        Get Receipt records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related cart data
        """
        receipts, http_code = self._get(id=id,
                                        with_relationships=relationships)
        return receipts, http_code

    @require_jwt("administrator")
    def post(self):
        data = request.get_json()
        new_record, http_code = self._add(data)
        return new_record, http_code
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update Receipt information (e.g., status or purchase_date).
        """
        data = request.get_json()
        updated_record, http_code = self._update(id, data)
        return updated_record, http_code
        
    
    @require_jwt("administrator")
    def delete(self, id):
        deleted_record, http_code = self._remove(id)
        return deleted_record, http_code
