from flask.views import MethodView
from flask import jsonify, request
from validators.validator import reject_fields
from api.controller import ApiRegistrationTransactions
from configurations.cache_config import cache_key_mapper
from flask_jwt_extended import (jwt_required, get_jwt_identity)


class ProductRegistration(MethodView):
    def __init__(self):
        self.option = "product_registration"
        self.api_transaction = ApiRegistrationTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @jwt_required()
    def get(self, id=None):
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code
    
    @jwt_required()
    @reject_fields("status", "id", "last_modified", "product_id", "inventory_id")
    def post(self):
        request_data = request.json
        msg, http_code = self.api_transaction._post(request_data)
        return jsonify(msg), http_code

    @jwt_required()
    @reject_fields("id", "last_modified", "ingress_date")
    def put(self, id):
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @jwt_required()
    def delete(self, id):
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code


class UserRegistration(MethodView):
    def __init__(self):
        self.option = "user_registration"
        self.api_transaction = ApiRegistrationTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @jwt_required()
    def get(self, id=None):
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code
    
    @jwt_required()
    @reject_fields("status", "id", "last_modified", "user_id", "")
    def post(self):
        request_data = request.json
        msg, http_code = self.api_transaction._post(request_data)
        return jsonify(msg), http_code

    @jwt_required()
    @reject_fields("id", "last_modified", "user_id")
    def put(self, id):
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @jwt_required()
    def delete(self, id):
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code