import json
from flask import (request, jsonify)
from datetime import date
from modules.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload



class RegistrationRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.manager = db_manager
        self.model_name = 'register_user'
        self.model_class = _models.get(self.model_name)

    def get_model(self):
        if not self.model_class:
            raise ValueError(f"Model '{self.model_name}' not found")
        return self.model_class

    def get(self, id=None, with_relationships=True):
        """
        Get registration records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
        """
        model_class = self.get_model()
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
            _query = _query.options(joinedload(model_class.user))
        
        results = self.manager.get(_query)
        
        # If querying by ID and no result found
        if id and not results:
            return jsonify({"error": "Registration not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        registration_list = []
        for reg in results:
            reg_data = {
                "registration_id": reg.id,
                "email": reg.email,
                "created_at": str(reg.created_at) if reg.created_at else None,
                "updated_at": str(reg.updated_at) if reg.updated_at else None
            }
            
            # Include related user data if loaded
            if with_relationships and hasattr(reg, 'user') and reg.user:
                reg_data["user"] = {
                    "id": reg.user.id,
                    "first_name": reg.user.first_name,
                    "last_name": reg.user.last_name
                }
            print(reg_data)
            registration_list.append(reg_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and registration_list:
            return jsonify(registration_list[0])
        
        return jsonify(registration_list)

    def post(self):
        data = request.get_json()
        fields = ["email", "password", "role"]
        for field in fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        # Validate password length
        if len(data['password']) > 8:
            return jsonify({"error": "Password must be 8 characters or less"}), 400
        try:
            session = self.manager.sessionlocal()
            model_class = self.get_model()
            new_record = model_class(**data)
            record = self.manager.insert(new_record, session)
            return jsonify({
                "id": record.id,
                "email": record.email,
                "role": record.role,
                "created_at": str(record.created_at)
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    def put(self, id):
        """
        Update registration information (e.g., change role or password).
        """
        model_class = self.get_model()
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            session = self.manager.sessionlocal()
            # Get fields to update (exclude id)
            update_data = {k: v for k, v in request.json.items() if k != 'id'}
            
            if not update_data:
                return jsonify({"error": "No fields to update"}), 400
            
            # Validate password length if updating password
            if 'password' in update_data and len(update_data['password']) > 8:
                return jsonify({"error": "Password must be 8 characters or less"}), 400
            
            # Update registration
            updated_reg = self.manager.update(session, model_class,
                                              id, **update_data)
            
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

    def delete(self, id):
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            model_class = self.get_model()
            session = self.manager.sessionlocal()
            message = self.manager.delete(session, model_class, id)
            return jsonify({"message": message}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
