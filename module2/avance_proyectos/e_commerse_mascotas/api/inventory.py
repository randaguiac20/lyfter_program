"""
inventory.py

Defines the InventoryAPI class for managing inventory-related endpoints.
Supports GET, POST, PUT, and DELETE operations for inventory items.
"""

from flask.views import MethodView
from flask import jsonify, request
from aaa.authorization import role_required
from validators.validator import reject_fields
from api.controller import ApiControllerTransactions
from configurations.cache_config import cache_key_mapper

class InventoryAPI(MethodView):
    """
    API endpoint for managing inventory items.

    Provides GET, POST, PUT, and DELETE methods for inventory data.
    """

    def __init__(self):
        """
        Initialize InventoryAPI with option, controller, and cache keys.
        """
        self.option = "inventory"
        self.api_transaction = ApiControllerTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @role_required(["administrator", "client"])
    def get(self, id=None):
        """
        Retrieve inventory item(s).

        Args:
            id (str, optional): Inventory item ID. If not provided, returns all items.

        Returns:
            Response: JSON response with inventory data and HTTP status code.
        """
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code

    @role_required(["administrator"])
    @reject_fields("status", "id", "last_modified")
    def post(self):
        """
        Create a new inventory item.

        Returns:
            Response: JSON response with creation status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._post(request_data)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    @reject_fields("id", "last_modified")
    def put(self, id):
        """
        Update an existing inventory item.

        Args:
            id (str): Inventory item ID.

        Returns:
            Response: JSON response with update status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    def delete(self, id):
        """
        Delete an inventory item.

        Args:
            id (str): Inventory item ID.

        Returns:
            Response: JSON response with delete status and HTTP status code.
        """
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code