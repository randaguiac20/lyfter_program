from flask.views import MethodView
from flask import jsonify, request
from validator import reject_fields
from user_transactions import UserRegistrationTransactions


class UserRegistration(MethodView):
    def __init__(self):
        self.user_transaction = UserRegistrationTransactions()

    def get(self, user_id=None):
        cache_key = f"user_{user_id}" if user_id else "all_users"
        data, http_code = self.user_transaction._get(user_id, cache_key)
        return jsonify(data), http_code
    
    @reject_fields("status", "user_id", "last_modified")
    def post(self):
        request_data = request.json
        msg, http_code = self.user_transaction._post(request_data)
        return jsonify(msg), http_code

    @reject_fields("user_id", "last_modified")
    def put(self, user_id):
        request_data = request.json
        msg, http_code = self.user_transaction._put(request_data, user_id)
        return jsonify(msg), http_code

    def delete(self, user_id):
        msg, http_code = self.user_transaction._delete(user_id)
        return jsonify(msg), http_code
