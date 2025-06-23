"""
registration.py

Defines the ProductRegistration and UserRegistration API classes for managing
product and user registration endpoints. Supports GET, POST, PUT, and DELETE
operations for both products and users.
"""

from flask.views import MethodView
from flask import jsonify, request
from validators.validator import reject_fields
from api.controller import ApiControllerTransactions
from configurations.cache_config import cache_key_mapper
from aaa.authorization import role_required


class ProductRegistration(MethodView):
    """
    API endpoint for managing product registration.

    Provides GET, POST, PUT, and DELETE methods for product registration data.
    """
    def __init__(self):
        """
        Initialize ProductRegistration with option, controller, and cache keys.
        """
        self.option = "product_registration"
        self.api_transaction = ApiControllerTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @role_required(["administrator", "client"])
    def get(self, id=None):
        """
        Retrieve product registration item(s).

        Args:
            id (str, optional): Product registration item ID. If not provided, returns all items.

        Returns:
            Response: JSON response with product registration data and HTTP status code.
        """
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code
    
    @role_required(["administrator"])
    @reject_fields("status", "id", "last_modified", "product_id", "inventory_id")
    def post(self):
        """
        Create a new product registration item.

        Returns:
            Response: JSON response with creation status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._post(request_data)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    @reject_fields("id", "last_modified", "ingress_date")
    def put(self, id):
        """
        Update an existing product registration item.

        Args:
            id (str): Product registration item ID.

        Returns:
            Response: JSON response with update status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    def delete(self, id):
        """
        Delete a product registration item.

        Args:
            id (str): Product registration item ID.

        Returns:
            Response: JSON response with delete status and HTTP status code.
        """
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code


class UserRegistration(MethodView):
    """
    API endpoint for managing user registration.

    Provides GET, POST, PUT, and DELETE methods for user registration data.
    """
    def __init__(self):
        """
        Initialize UserRegistration with option, controller, and cache keys.
        """
        self.option = "user_registration"
        self.api_transaction = ApiControllerTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @role_required(["administrator", "client"])
    def get(self, id=None):
        """
        Retrieve user registration item(s).

        Args:
            id (str, optional): User registration item ID. If not provided, returns all items.

        Returns:
            Response: JSON response with user registration data and HTTP status code.
        """
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code
    
    @role_required(["administrator"])
    @reject_fields("status", "id", "last_modified", "user_id", "")
    def post(self):
        """
        Create a new user registration item.

        Returns:
            Response: JSON response with creation status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._post(request_data)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    @reject_fields("id", "last_modified", "user_id")
    def put(self, id):
        """
        Update an existing user registration item.

        Args:
            id (str): User registration item ID.

        Returns:
            Response: JSON response with update status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    def delete(self, id):
        """
        Delete a user registration item.

        Args:
            id (str): User registration item ID.

        Returns:
            Response: JSON response with delete status and HTTP status code.
        """
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code