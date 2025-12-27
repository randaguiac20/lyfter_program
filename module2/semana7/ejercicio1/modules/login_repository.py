import json
from flask import (request, jsonify)
from datetime import date
from modules.repository import Repository
from modules.models import _models
from sqlalchemy.orm import joinedload
from modules.jwt_manager import require_jwt, JWT_Manager
from modules.secret_keys import verify_password



class LoginRepository(Repository):
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

    @require_jwt(["administrator", "client"])
    def get(self):
        session = self.manager.sessionlocal()
        model_class = self._get_model()
        _token = request.headers.get("Authorization")
        token = _token.replace("Bearer ","")
        if not token:
            return jsonify({"error": "No token provided"}), 400

        jwt_manager = JWT_Manager()
        decoded = jwt_manager.decode(token)
        email = decoded.get("email")
        _query = session.query(model_class).filter_by(email=email)
        record = self.manager.get(_query)
        return jsonify({
            "email": record.email,
            "created_at": str(record.created_at)
        })

    @require_jwt(["administrator", "client"])
    def post(self):
        session = self.manager.sessionlocal()
        model_class = self._get_model()
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        _query = session.query(model_class).filter_by(email=email)
        records = self.manager.get(_query)
        if not records or len(records) == 0:
            return jsonify({"error": "User not found"}), 404
        record = records[0]
        hashed = record.password
        is_valid = verify_password(hashed, password)
        if not is_valid:
            return jsonify({"error": "Invalid password"}), 403
        jwt_manager = JWT_Manager()
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
