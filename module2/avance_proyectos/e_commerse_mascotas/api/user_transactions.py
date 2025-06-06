from flask.views import MethodView
from flask import request
from schema_validator import schema_validator
from db_connector import DataManager
from config import USERS_REGISTRATION_DIR
from datetime import datetime
from cache_config import cache
import uuid


class UserRegistrationTransactions:
    def __init__(self):
        self.user_schema = schema_validator
        self.db = DataManager()
        self.user_registration_dir = USERS_REGISTRATION_DIR
        
    def _get(self, user_id, cache_key):
        _data = cache.get(cache_key)
        if user_id:
            if _data:
                return _data, 200
            user_registration_id = f"{self.user_registration_dir}/{user_id}.json"
            data, http_code = self.db.get_registered_user(user_registration_id)
            if http_code == 200:
                cache.set(cache_key, data)
            return data, http_code
        data, http_code = self.db.get_registered_users(self.user_registration_dir)
        if _data is None:
            cache.set(cache_key, data)
        else:
            data = _data
        filter_status = request.headers.get("status")
        if filter_status:
            data = list(
            filter(lambda _status: _status["status"] == filter_status, data)
            )
        return data, http_code
    
    def _post(self, request_data):
        directory_path = self.user_registration_dir
        request_data['user_id'] = str(uuid.uuid4())
        request_data['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        request_data['status'] = "registered"
        schema_true, msg = self.user_schema("user_registration", request_data)
        if schema_true is False:
            return msg, 400
        file_id = request_data.get('user_id')
        user_filename = f"{self.user_registration_dir}/{file_id}.json"
        msg, http_code = self.db.save_user_registration(request_data, filepath=user_filename,
                                                        directory_path=directory_path)
        return msg, http_code

        
    def _put(self, request_data, user_id):
        user_registration_id = f"{self.user_registration_dir}/{user_id}.json"
        data, http_code = self.db.get_registered_user(user_registration_id)
        request_data['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        data.update(request_data)
        schema_true, msg = self.user_schema("user_registration", data)
        if schema_true is False:
            return msg, 400
        true_false, data = self.db.update_registered_user(data, user_registration_id)
        if true_false is False:
            msg = f"User ID {data.get("user_id")} was not updated."
            return msg, 404
        schema_true, msg = self.user_schema("user_registration", data)
        if schema_true is False:
            return msg, 400
        msg = f"User ID {data.get("user_id")} was updated."
        # Invalidate caches
        cache.delete("all_users")
        cache.delete(f"user_{user_id}")
        return msg, 200

    def _delete(self, user_id):
        user_registration_id = f"{self.user_registration_dir}/{user_id}.json"
        msg, http_code = self.db.delete_user(user_registration_id)
        # Invalidate caches
        if http_code != 200:
            cache.delete("all_users")
            cache.delete(f"user_{user_id}")
        return msg, http_code