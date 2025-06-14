from flask.views import MethodView
from flask import jsonify, request
from aaa.authorization import role_required
from validators.validator import reject_fields
from api.controller import ApiControllerTransactions
from configurations.cache_config import cache_key_mapper

class UsersAPI(MethodView):
    """
    API endpoint for managing user profiles.

    Provides GET, PUT, and DELETE methods for user data.
    """

    def __init__(self):
        """
        Initialize UsersAPI with option, controller, and cache keys.
        """
        self.option = "users"
        self.api_transaction = ApiControllerTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @role_required(["administrator"])
    def get(self, id=None):
        """
        Retrieve user(s) information.

        Args:
            id (str, optional): User ID. If not provided, returns all users.

        Returns:
            Response: JSON response with user data and HTTP status code.
        """
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code

    @role_required(["administrator"])
    @reject_fields("id", "last_modified", "user_id")
    def put(self, id):
        """
        Update user information.

        Args:
            id (str): User ID.

        Returns:
            Response: JSON response with update status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    def delete(self, id):
        """
        Delete a user.

        Args:
            id (str): User ID.

        Returns:
            Response: JSON response with delete status and HTTP status code.
        """
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code