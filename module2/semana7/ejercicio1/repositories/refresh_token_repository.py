import json
from flask import (request, jsonify)
from repositories.repository import Repository
from modules.models import _models
from modules.jwt_manager import require_jwt, JWT_Manager



class RefreshTokenRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.db_manager = db_manager
        self.model_name = self.db_manager._get_model_name('register_user')
        self.model_class = self.db_manager._get_model()

    @require_jwt(["administrator", "client"])
    def post(self):
        model_class = self.model_class
        session = self.db_manager.sessionlocal()
        
        _token = request.headers.get("Authorization")
        _token = _token.replace("Bearer ","")
        if not _token:
            return jsonify({"error": "No token provided"}), 400
        
        jwt_manager = JWT_Manager()
        decoded = jwt_manager.decode(_token)
        email = decoded.get("email")
        _query = session.query(model_class).filter_by(email=email)
        records = self.db_manager.get_query(_query)
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