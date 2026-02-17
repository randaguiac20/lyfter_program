"""registration_repository.py

User registration repository for managing user authentication records.
Handles CRUD operations for user registration including email, password, and role management.
"""

import json
from flask import (request, jsonify)
from repositories.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt, JWT_Manager
from modules.secret_keys import password_hash, verify_password
from modules.config import ALLOWED_ROLES
from modules.models import _models



class RegistrationRepository(Repository):
    """
    Repository for managing user registrations.
    
    Handles user authentication data including email, hashed passwords, and roles.
    Provides CRUD operations with JWT token generation on registration.
    
    Attributes:
        db_manager: Database manager instance.
        model_class: The UserRegistration model class.
    """
    
    def __init__(self, db_manager, *args, **kwargs):
        """
        Initialize the registration repository.
        
        Args:
            db_manager: Database manager instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_class = _models.get('register_user')
    
    def _get(self, id=None, email=None):
        """
        Internal method to retrieve registration records.
        
        Args:
            id (int, optional): Filter by registration ID.
            email (str, optional): Filter by email address.
            
        Returns:
            tuple: (JSON response, HTTP status code)
        """
        model_class = self.model_class
        relationship_list = [model_class.user]
        session = self.db_manager.sessionlocal()
        registrations = self.db_manager.get_query(session, model_class, id=id, email=email,
                                                  relationships=relationship_list)
        
        # If querying by ID and no result found
        if id and not registrations:
            return jsonify({"error": "Registration not found"}), 404
        
        # Convert SQLAlchemy objects to dictionaries
        registration_list = []
        for registration in registrations:
            reg_data = {
                "registration_id": registration.id,
                "email": registration.email,
                "created_at": str(registration.created_at) if registration.created_at else None,
                "updated_at": str(registration.updated_at) if registration.updated_at else None
            }
            
            # Include related user data if loaded
            if hasattr(registration, 'user') and registration.user:
                reg_data["user"] = {
                    "id": registration.user.id,
                    "user_name": f"{registration.user.first_name} {registration.user.last_name}"
                }
            registration_list.append(reg_data)
        
        # Return single object if querying by ID, otherwise return list
        if id and registration_list:
            return jsonify(registration_list[0]), 200
        
        return jsonify(registration_list), 200

    def _add(self, data):
        """
        Internal method to create a new registration.
        
        Validates required fields, hashes password, creates registration,
        and generates JWT token.
        
        Args:
            data (dict): Registration data with 'email', 'password', and 'role'.
            
        Returns:
            tuple: (JSON response with id, created_at, and token, HTTP status code)
        """
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
            
            _registration = model_class(**hashed_data)
            registration = self.db_manager.insert(session, _registration)
            
            # Generate JWT token for the newly registered user
            jwt_manager = JWT_Manager()
            
            # Create token data
            token_data = {
                "id": registration.id,
                "email": registration.email,
                "role": registration.role
            }
            token = jwt_manager.encode(token_data)
            
            return jsonify({
                "id": registration.id,
                "created_at": str(registration.created_at),
                "token": token
            }), 201
        except Exception as e:
            return jsonify({"error": "User is already registered"}), 400

    def _update(self, id, data):
        """
        Internal method to update a registration record.
        
        Allows updating email, password (re-hashed), and role.
        
        Args:
            id (int): Registration ID to update.
            data (dict): Fields to update.
            
        Returns:
            tuple: (JSON response, HTTP status code)
        """
        if not data:
            return jsonify({"error": "No fields to update"}), 400
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            registrations = self.db_manager.get_query(session, model_class, id=id)
            registration = registrations[0]
            if not registration:
                return jsonify({"error": f"User ID {id} has not been found"}), 404
            # Update fields directly on the existing record
            if 'email' in data:
                registration.email = data['email']
            if 'password' in data:
                # Hash the new password
                registration.password = password_hash(data['password'])
            if 'role' in data:
                if not data['role'] in ALLOWED_ROLES:
                    return jsonify({"error": "Invalid role was provided"}), 400
                registration.role = data['role']

            # Update registration
            updated_reg = self.db_manager.update(session, registration)
            if updated_reg:
                return jsonify({
                    "id": updated_reg.id,
                    "email": updated_reg.email,
                    "role": updated_reg.role,
                    "updated_at": str(updated_reg.updated_at)
                }), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def _remove(self, id):
        """
        Internal method to delete a registration record.
        
        Args:
            id (int): Registration ID to delete.
            
        Returns:
            tuple: (JSON response with deletion message, HTTP status code)
        """
        if not id:
            return jsonify({"error": "Registration ID is required"}), 400
        try:
            model_class = self.model_class
            session = self.db_manager.sessionlocal()
            registrations = self.db_manager.get_query(session, model_class, id=id)
            registration = registrations[0]
            if not registration:
                raise ValueError(f"User ID {id} has not been found")
            self.db_manager.delete(session, registration)
            msg = f"Register User with ID {id}, and email {registration.email} has been DELETED"
            return jsonify({"message": msg}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @require_jwt("administrator")
    def get(self, id=None, email=None):
        """
        Get registration records.
        
        Args:
            id: Optional ID from URL path parameter
            with_relationships: Whether to load related user data
        """
        records, http_code = self._get(id=id, email=email)
        return records, http_code
    
    @require_jwt("administrator")
    def post(self):
        """
        Create a new user registration.
        
        Requires administrator role. Creates registration with email,
        password, and role.
        
        Returns:
            tuple: (JSON response with new registration data, HTTP status code)
        """
        data = request.get_json()
        new_record, http_code = self._add(data)
        return new_record, http_code

    @require_jwt("administrator")
    def put(self, id):
        """
        Update registration information (e.g., change role or password).
        """
        data = request.get_json()
        updated_record, http_code = self._update(id, data)
        return updated_record, http_code

    @require_jwt("administrator")
    def delete(self, id):
        deleted_record, http_code = self._remove(id)
        return deleted_record, http_code
