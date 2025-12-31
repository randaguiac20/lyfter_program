import json
from flask import (Flask, request, jsonify)
from datetime import date
from modules.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt



class UserRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.manager = db_manager
        self.model_name = 'user'
        self.model_class = _models.get(self.model_name)

    def _get_model(self):
        if not self.model_class:
            raise ValueError(f"Model '{self.model_name}' not found")
        return self.model_class

    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get user records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
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
            _query = _query.options(joinedload(model_class.contacts),
                                    joinedload(model_class.address),
                                    joinedload(model_class.carts))
        
        users = self.manager.get(_query)
        
        # If querying by ID and no result found
        if id and not users:
            return jsonify({"error": "Registration not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        user_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "registration_id": user.registration_id,
                "email": user.email,
                "user name": f"{user.first_name} {user.last_name}",
                "created_at": str(user.created_at) if user.created_at else None,
                "updated_at": str(user.updated_at) if user.updated_at else None
            }
            
            # Include related user data if loaded
            if with_relationships and hasattr(user, 'contacts') and user.contacts:
                print(user_data['contacts'])
                user_data["contacts"] = {
                    "id": user.contacts.id,
                    "first_name": user.contacts.first_name,
                    "last_name": user.contacts.last_name,
                    "email": user.contacts.email
                }
            
            user_list.append(user_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and user_list:
            return jsonify(user_list[0])
        
        return jsonify(user_list)

    @require_jwt("administrator")
    def post(self):
        session = self.manager.sessionlocal()
        model_class = self._get_model()
        data = request.get_json()
        new_record = model_class(**data)
        record = self.manager.insert(session, new_record)
        
        if record is None:
            return jsonify({
            "error": "User already exists or violates database constraints",
            "message": "This user may already be registered or the data conflicts with existing records"
        }), 409
        return jsonify({
            "email": record.email,
            "first_name": record.first_name,
            "last_name": record.last_name,
            "created_at": str(record.created_at)
        })
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update User information (e.g., change role or password).
        """
        data = request.get_json()
        if not data:
            return jsonify({"error": "No fields to update"}), 400
        model_class = self._get_model()
        new_record = model_class(**data)
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            session = self.manager.sessionlocal()
            _query = session.query(model_class).filter_by(id=id)
            records = self.manager.get(_query)
            current_record = records[0]
            import ipdb; ipdb.set_trace()
            # Get fields to update (exclude id)
            update_data = {k: v for k, v in request.json.items() if k != 'id'}
            
            if not update_data:
                return jsonify({"error": "No fields to update"}), 400
            
            # Update registration
            updated_reg = self.manager.update(session, new_record)
            
            return jsonify({
                "id": updated_reg.id,
                "email": updated_reg.email,
                "role": updated_reg.role,
                "updated_at": str(updated_reg.updated_at)
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
            model_class = self._get_model()
            session = self.manager.sessionlocal()
            message = self.manager.delete(session, model_class, id)
            return jsonify({"message": message}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
