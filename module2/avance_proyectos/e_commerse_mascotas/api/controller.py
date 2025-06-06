from flask.views import MethodView
from flask import request
from validators.schema_validator import schema_validator
from data_manager.db_connector import DataManager
from configurations.config import directory_mapper
from configurations.cache_config import cache
from datetime import datetime
import uuid


class ApiRegistrationTransactions:
    def __init__(self, option):
        self.schema = schema_validator
        self.db = DataManager()
        self.directory = directory_mapper.get(option)
        self.option = option
        
    def _get(self, id, cache_key):
        _data = cache.get(cache_key)
        if id:
            if _data:
                return _data, 200
            registration_id = f"{self.directory}/{id}.json"
            data, http_code = self.db.get_data_item(registration_id)
            if http_code == 200:
                cache.set(cache_key, data)
            return data, http_code
        data, http_code = self.db.get_data_items(self.directory)
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
        dir_path = self.directory
        if self.option == "product_registration":
            request_data['product_id'] = str(uuid.uuid4())
            request_data['inventory_id'] = str(uuid.uuid4())
        if self.option == "user_registration":
            request_data['user_id'] = str(uuid.uuid4())
        request_data['id'] = str(uuid.uuid4())
        request_data['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        request_data['status'] = "registered"
        schema_true, msg = self.schema(self.option, request_data)
        if schema_true is False:
            return msg, 400
        file_id = request_data.get('id')
        filename = f"{self.directory}/{file_id}.json"
        msg, http_code = self.db.save_registration_data(request_data, filepath=filename,
                                                        directory_path=dir_path, option=self.option)
        return msg, http_code

        
    def _put(self, request_data, id, cache_keys):
        registration_id = f"{self.directory}/{id}.json"
        data, http_code = self.db.save_registration_data(registration_id, option=self.option)
        request_data['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        data.update(request_data)
        schema_true, msg = self.schema(self.option, data)
        if schema_true is False:
            return msg, 400
        true_false, data = self.db.update_registered_user(data, user_registration_id)
        if true_false is False:
            msg = f"{self.option} {data.get("id")} was not updated."
            return msg, 404
        schema_true, msg = self.schema(self.option, data)
        if schema_true is False:
            return msg, 400
        msg = f"{self.option} {data.get("id")} was updated."
        # Invalidate caches
        cache.delete(cache_keys[0])
        cache.delete(f"{cache_keys[1]}_{id}")
        return msg, 200

    def _delete(self, id, cache_keys):
        user_registration_id = f"{self.directory}/{id}.json"
        msg, http_code = self.db.delete_data(user_registration_id, self.option)
        # Invalidate caches
        if http_code != 200:
            cache.delete(cache_keys[0])
            cache.delete(f"{cache_keys[1]}_{id}")
        return msg, http_code