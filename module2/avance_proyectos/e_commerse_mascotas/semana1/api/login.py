"""
login.py

Defines the LoginAPI class for handling user authentication.
Provides the POST endpoint for user login and JWT token generation.
"""

from flask.views import MethodView
from flask import jsonify, request
from validators.validator import reject_fields
from werkzeug.security import check_password_hash
from api.controller import LoginAPITransactions

class LoginAPI(MethodView):
    """
    API endpoint for user login and authentication.

    Provides a POST method to authenticate users and return a JWT token.
    """
    def __init__(self):
        """
        Initialize LoginAPI with the user option and login transaction handler.
        """
        self.option = "users"
        self.api_login = LoginAPITransactions(self.option)

    def post(self):
        """
        Authenticate a user and return a JWT token.

        Returns:
            Response: JSON response with token or error message and HTTP status code.
        """
        data = request.get_json()
        msg, http_code = self.api_login._post(data)
        return jsonify(msg), http_code