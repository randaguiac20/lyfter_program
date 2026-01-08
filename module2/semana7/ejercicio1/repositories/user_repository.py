import json
from flask import (Flask, request, jsonify)
from datetime import date
from repositories.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt



class UserRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('user')
        self.model_class = self.db_manager._get_model()

    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get user records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
        """
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        # If id is provided, try to get by ID
        if id:
            try:
                id = int(id)
                users = self.db_manager.get_by_id(session, id)
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400
        else:
            users = self.db_manager.get_query(session)
            
        if with_relationships:
            _query = session.query(model_class)
            _query_with_options = _query.options(joinedload(model_class.contacts),
                                                 joinedload(model_class.address),
                                                 joinedload(model_class.carts))
            users = self.db_manager.get(_query_with_options)
        
        # If querying by ID and no result found
        if id and not users:
            return jsonify({"error": "Registration not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        user_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "registration_id": user.registration_id,
                "user_name": f"{user.first_name} {user.last_name}",
                "created_at": str(user.created_at) if user.created_at else None,
                "updated_at": str(user.updated_at) if user.updated_at else None
            }
            # Include related address data if loaded
            if with_relationships and hasattr(user, 'address') and user.address:
                user_data["address"] = {
                    "id": user.address.id,
                    "street": user.address.street,
                    "city": user.address.city,
                    "state": user.address.state,
                    "postal_code": user.address.postal_code,
                    "country": user.address.country
                }
            # Include related contact data if loaded
            if with_relationships and hasattr(user, 'contacts') and user.contacts:
                contact_list = []
                for contact in user.contacts:
                    contact_data = {
                        "contact_id": contact.id,
                        "user_name": f"{user.first_name} {user.last_name}"
                    }
                    contact_list.append(contact_data)
                user_data["contacts"] = contact_list
            
            # Include related cart data if loaded
            if with_relationships and hasattr(user, 'carts') and user.carts:
                cart_list = []
                for cart in user.carts:
                    cart_data = {
                        "cart_id": cart.id,
                        "status": cart.status,
                        "purchase_date": cart.purchase_date
                    }
                    cart_list.append(cart_data)
                user_data['carts'] = cart_list
            
            user_list.append(user_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and user_list:
            return jsonify(user_list[0])
        
        return jsonify(user_list)

    @require_jwt("administrator")
    def post(self):
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        data = request.get_json()
        new_record = model_class(**data)
        record = self.db_manager.insert(session, new_record)
        
        if record is None:
            return jsonify({
            "error": "User already exists or violates database constraints",
            "message": "This user may already be registered or the data conflicts with existing records"
        }), 409
        return jsonify({
            "id": record.id,
            "first_name": record.first_name,
            "last_name": record.last_name,
            "created_at": str(record.created_at)
        })
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update User information (e.g., change role or password).
        """
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "No fields to update"}), 400
        
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, id)
            record = records[0]
            if not record:
                return jsonify({"error": f"User ID {id} has not been found"}), 404
            
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
            if updated_user:
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
            return jsonify({"error": "User ID is required"}), 400
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, id)
            record = records[0]
            if not record:
                raise ValueError(f"User ID {id} has not been found")
            self.db_manager.delete(session, record)
            msg = f"User with ID {id}, and email {record.email} has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
