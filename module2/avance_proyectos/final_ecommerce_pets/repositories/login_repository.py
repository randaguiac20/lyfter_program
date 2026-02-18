"""login_repository.py

Login repository handling user authentication.
Provides endpoints for user login and retrieving current user information.
"""

import json
from flask import (request, jsonify)
from repositories.repository import Repository
from modules.jwt_manager import require_jwt, JWT_Manager
from modules.secret_keys import verify_password



class LoginRepository(Repository):
    """
    Repository for handling user authentication.
    
    Provides login functionality and current user info retrieval.
    Uses JWT tokens for authentication.
    
    Attributes:
        db_manager: Database manager instance.
        model_name: The model name for user registration.
    """
    
    def __init__(self, db_manager, *args, **kwargs):
        """
        Initialize the login repository.
        
        Args:
            db_manager: Database manager instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('register_user')

    @require_jwt(["administrator", "client"])
    def get(self,):
        """
        Get current authenticated user information.
        
        Extracts user email from JWT token and retrieves user details.
        Requires valid JWT token with 'administrator' or 'client' role.
        
        Returns:
            tuple: JSON response with user email and creation date, HTTP status code.
        """
        session = self.db_manager.sessionlocal()
        _token = request.headers.get("Authorization")
        token = _token.replace("Bearer ","")
        if not token:
            return jsonify({"error": "No token provided"}), 400
        jwt_manager = JWT_Manager()
        decoded = jwt_manager.decode(token)
        email = decoded.get("email")
        records = self.db_manager.get_by_email(session, email)
        record = records[0]
        if not record:
            return jsonify({"error": f"No record found for {email}"}), 404
        return jsonify({
            "email": record.email,
            "created_at": str(record.created_at)
        }), 200
    
    def post(self):
        """
        Authenticate user and generate JWT token.
        
        Validates email and password, returns JWT access token on success.
        
        Request Body:
            email (str): User's email address.
            password (str): User's password.
            
        Returns:
            tuple: JSON response with email, token, and creation date on success,
                   or error message with appropriate HTTP status code.
        """
        session = self.db_manager.sessionlocal()
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        records = self.db_manager.get_by_email(session, email)
        
        if not records or len(records) == 0:
            return jsonify({"error": "User not found"}), 404
        record = records[0]
        hashed = record.password
        is_valid = verify_password(hashed, password)
        
        if not is_valid:
            return jsonify({"error": "Invalid password"}), 403
        jwt_manager = JWT_Manager()

        # Create token data
        token_data = {
                "id": record.id,
                "email": record.email,
                "role": record.role
            }
        token = jwt_manager.encode(token_data)
        return jsonify({
            "email": record.email,
            "token": token,
            "created_at": str(record.created_at)
        })

    def put(self):
        pass

    def delete(self):
        pass