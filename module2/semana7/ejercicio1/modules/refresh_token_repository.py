import json
from flask import (request, jsonify)
from modules.repository import Repository
from modules.models import _models
from modules.jwt_manager import require_jwt, JWT_Manager



class RefreshTokenRepository(Repository):
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
    def post(self):
        session = self.manager.sessionlocal()
        model_class = self._get_model()
        _token = request.headers.get("Authorization")
        _token = _token.replace("Bearer ","")
        if not _token:
            return jsonify({"error": "No token provided"}), 400
        
        jwt_manager = JWT_Manager()
        decoded = jwt_manager.decode(_token)
        email = decoded.get("email")
        _query = session.query(model_class).filter_by(email=email)
        records = self.manager.get(_query)
        record = records[0]
        if not records or len(records) == 0:
            return jsonify({"error": "User not found"}), 404
        token_data = {
                "id": record.id,
                "email": record.email,
                "role": record.role
            }
        access_token = jwt_manager.encode(token_data)
        refresh_token = jwt_manager.encode_refresh_token(email=email)
        return jsonify({
            "email": record.email,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "created_at": str(record.created_at)
        })

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass