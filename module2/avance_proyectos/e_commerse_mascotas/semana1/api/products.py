"""
products.py

Defines the ProductAPI class for managing product-related endpoints.
Supports GET, PUT, and DELETE operations for product items.
"""

from flask.views import MethodView
from flask import jsonify, request
from aaa.authorization import role_required
from validators.validator import reject_fields
from api.controller import ApiControllerTransactions
from configurations.cache_config import cache_key_mapper


class ProductAPI(MethodView):
    """
    API endpoint for managing product items.

    Provides GET, PUT, and DELETE methods for product data.
    """

    def __init__(self):
        """
        Initialize ProductAPI with option, controller, and cache keys.
        """
        self.option = "products"
        self.api_transaction = ApiControllerTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @role_required(["administrator", "client"])
    def get(self, id=None):
        """
        Retrieve product item(s).

        Args:
            id (str, optional): Product item ID. If not provided, returns all items.

        Returns:
            Response: JSON response with product data and HTTP status code.
        """
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code
    
    # THIS HTTP METHOD IS NOT REALLY NEEDED
    # BECAUSE ONCE PRODUCT IS REGISTERED, THE PRODUCT PROFILE
    # IS CREATED AUTOMATICALLY, AND ALL WE NEED TO DO IS
    # TO CHANGE THE STATUS FROM DISABLE TO ACTIVE WITH PUT METHOD
    # @role_required(["administrator"])
    # @reject_fields("status", "id", "last_modified", "product_id", "inventory_id")
    # def post(self):
    #     """
    #     Create a new product item.
    #
    #     Returns:
    #         Response: JSON response with creation status and HTTP status code.
    #     """
    #     request_data = request.json
    #     msg, http_code = self.api_transaction._post(request_data)
    #     return jsonify(msg), http_code

    @role_required(["administrator"])
    @reject_fields("id", "last_modified", "ingress_date")
    def put(self, id):
        """
        Update an existing product item.

        Args:
            id (str): Product item ID.

        Returns:
            Response: JSON response with update status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    def delete(self, id):
        """
        Delete a product item.

        Args:
            id (str): Product item ID.

        Returns:
            Response: JSON response with delete status and HTTP status code.
        """
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code