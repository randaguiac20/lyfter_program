import json
from flask import (request, jsonify)
from repositories.repository import Repository
from modules.jwt_manager import require_jwt, JWT_Manager
from modules.secret_keys import verify_password



class LoginRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('register_user')

    @require_jwt(["administrator", "client"])
    def get(self,):
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
        })
    
    def post(self):
        session = self.db_manager.session
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        records = self.db_manager.get_by_email(session, email)
        record = records[0]
        if not records or len(records) == 0:
            return jsonify({"error": "User not found"}), 404
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