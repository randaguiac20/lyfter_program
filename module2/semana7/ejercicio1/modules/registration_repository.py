import json
from flask import (request, jsonify)
from modules.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt, JWT_Manager
from modules.secret_keys import password_hash, verify_password



class RegistrationRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.manager = db_manager
        self.model_name = 'register_user'
        self.model_class = _models.get(self.model_name)

    def _get_model(self):
        if not self.model_class:
            raise ValueError(f"Model '{self.model_name}' not found")
        return self.model_class
    
    @require_jwt("administrator")
    def get(self, id=None, with_relationships=True):
        """
        Get registration records.
        
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
            _query = _query.options(joinedload(model_class.user))
        
        registrations = self.manager.get(_query)
        
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
            session = self.manager.sessionlocal()
            model_class = self._get_model()
            new_record = model_class(**hashed_data)
            record = self.manager.insert(session, new_record)
            
            # Generate JWT token for the newly registered user
            jwt_manager = JWT_Manager()
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
        model_class = self._get_model()
        _updated_record = model_class(**data)
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            session = self.manager.sessionlocal()
            _query = session.query(model_class).filter_by(id=id)
            records = self.manager.get(_query)
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
                record.role = data['role']

            # Update registration
            updated_reg = self.manager.update(session, record)
            
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
            model_class = self._get_model()
            session = self.manager.sessionlocal()
            record = session.query(model_class).filter_by(id=id).first()
            if not record:
                raise ValueError(f"User ID {id} has not been found")
            message = self.manager.delete(session, record)
            return jsonify({"message": message}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
