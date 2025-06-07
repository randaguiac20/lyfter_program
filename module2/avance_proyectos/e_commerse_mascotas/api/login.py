from flask.views import MethodView
from flask import jsonify, request
from validators.validator import reject_fields
from werkzeug.security import check_password_hash
from api.controller import LoginAPITransactions


class LoginAPI(MethodView):
    def __init__(self):
        self.option = "user"
        self.api_login = LoginAPITransactions(self.option)

    def post(self):
        data = request.get_json()
        msg, http_code = self.api_login._post(data)
        return jsonify(msg), http_code
        