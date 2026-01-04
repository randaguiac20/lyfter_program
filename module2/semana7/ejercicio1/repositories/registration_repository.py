import json
from flask import (request, jsonify)
from repositories.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt, JWT_Manager
from modules.secret_keys import password_hash, verify_password
from modules.config import ALLOWED_ROLES



class RegistrationRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('register_user')
        self.model_class = self.db_manager._get_model()
    
    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get registration records.
        
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
                registrations = self.db_manager.get_by_id(session, id)
            except ValueError:
                return jsonify({"error": "Invalid ID format"}), 400
        else:
            registrations = self.db_manager.get_query(session)
        
        if with_relationships:
            _query = session.query(model_class)
            _query_with_options = _query.options(joinedload(model_class.user))
            registrations = self.db_manager.get_query(_query_with_options)
        
        # If querying by ID and no result found
        if id and not registrations:
            return jsonify({"error": "Registration not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        registration_list = []
        for reg in registrations:
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
            registration_list.append(reg_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and registration_list:
            return jsonify(registration_list[0])
        
        return jsonify(registration_list)
    
    @require_jwt("administrator")
    def post(self):
        data = request.get_json()
        fields = ["email", "password", "role"]
        for field in fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Hash the password before storing
        hashed_data = data.copy()
        hashed_data['password'] = password_hash(data['password'])
        
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            
            new_record = model_class(**hashed_data)
            record = self.db_manager.insert(session, new_record)
            
            # Generate JWT token for the newly registered user
            jwt_manager = JWT_Manager()
            
            # Create token data
            token_data = {
                "id": record.id,
                "email": record.email,
                "role": record.role
            }
            token = jwt_manager.encode(token_data)
            
            return jsonify({
                "id": record.id,
                "created_at": str(record.created_at),
                "token": token
            }), 201
        except Exception as e:
            return jsonify({"error": "User is already registered"}), 400
    
    @require_jwt("administrator")
    def put(self, id):
        """
        Update registration information (e.g., change role or password).
        """
        data = request.get_json()
        if not data:
            return jsonify({"error": "No fields to update"}), 400
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            session = self.db_manager.sessionlocal()
            _query = self.db_manager.get_by_id(id)
            records = self.db_manager.get_query(_query)
            record = records[0]
            if not records:
                return jsonify({"error": f"User ID {id} has not been found"}), 404
            # Update fields directly on the existing record
            if 'email' in data:
                record.email = data['email']
            if 'password' in data:
                # Hash the new password
                record.password = password_hash(data['password'])
            if 'role' in data:
                if not data['role'] in ALLOWED_ROLES:
                    return jsonify({"error": "Invalid role was provided"}), 400
                record.role = data['role']

            # Update registration
            updated_reg = self.db_manager.update(session, record)
            if updated_reg:
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
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            session = self.db_manager.sessionlocal()
            records = self.db_manager.get_by_id(session, id)
            record = records[0]
            if not record:
                raise ValueError(f"User ID {id} has not been found")
            self.db_manager.delete(session, record)
            msg = f"Register User with ID {id}, and email {record.email} has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
