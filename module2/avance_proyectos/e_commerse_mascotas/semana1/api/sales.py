"""
sales.py

Defines API classes for managing sales, carts, and receipts endpoints.
Supports GET, POST, PUT, and DELETE operations for each entity.
"""

from flask.views import MethodView
from flask import jsonify, request
from aaa.authorization import role_required
from validators.validator import reject_fields
from api.controller import ApiControllerTransactions
from configurations.cache_config import cache_key_mapper


class SalesAPI(MethodView):
    """
    API endpoint for managing sales.

    Provides GET, POST, PUT, and DELETE methods for sales data.
    """
    def __init__(self):
        """
        Initialize SalesAPI with option, controller, and cache keys.
        """
        self.option = "sales"
        self.api_transaction = ApiControllerTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @role_required(["administrator", "client"])
    def get(self, id=None):
        """
        Retrieve sales record(s).

        Args:
            id (str, optional): Sales record ID. If not provided, returns all records.

        Returns:
            Response: JSON response with sales data and HTTP status code.
        """
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code

    @role_required(["administrator"])
    @reject_fields("status", "id", "last_modified")
    def post(self):
        """
        Create a new sales record.

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
        Update an existing sales record.

        Args:
            id (str): Sales record ID.

        Returns:
            Response: JSON response with update status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    def delete(self, id):
        """
        Delete a sales record.

        Args:
            id (str): Sales record ID.

        Returns:
            Response: JSON response with delete status and HTTP status code.
        """
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code

class CartsAPI(MethodView):
    """
    API endpoint for managing carts.

    Provides GET, POST, PUT, and DELETE methods for cart data.
    """
    def __init__(self):
        """
        Initialize CartsAPI with option, controller, and cache keys.
        """
        self.option = "carts"
        self.api_transaction = ApiControllerTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @role_required(["administrator", "client"])
    def get(self, id=None):
        """
        Retrieve cart(s).

        Args:
            id (str, optional): Cart ID. If not provided, returns all carts.

        Returns:
            Response: JSON response with cart data and HTTP status code.
        """
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code

    @role_required(["administrator"])
    @reject_fields("id", "last_modified")
    def post(self):
        """
        Create a new cart.

        Returns:
            Response: JSON response with creation status and HTTP status code.
        """
        request_data = request.json
        cart_msg, cart_http_code = self.api_transaction._post(request_data)
        return jsonify(cart_msg), cart_http_code

    @role_required(["administrator"])
    @reject_fields("id", "last_modified", "receipt_id", "sale_id", "status")
    def put(self, id):
        """
        Update an existing cart. Handles checkout logic and product updates.

        Args:
            id (str): Cart ID.

        Returns:
            Response: JSON response with update status and HTTP status code.
        """
        request_data = request.json
        if request_data.get("checkout") == "True" or \
           request_data.get("checkout") == "True" and request_data.get("products"):
            msg, http_code = self.api_transaction._update_cart_dependencies(request_data, id, self.cache_keys)
            return jsonify(msg), http_code
        elif request_data.get("checkout") == "False" and request_data.get("products"):
            msg, http_code = self.api_transaction._update_cart_dependencies(request_data, id, self.cache_keys)
            return jsonify(msg), http_code
        elif request_data.get("checkout") == "False":
            msg = {"message": f"Cart requires the product information to properly update cart dependencies."}
            return jsonify(msg), 406
        else:
            msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
            return jsonify(msg), http_code

    @role_required(["administrator"])
    def delete(self, id):
        """
        Delete a cart.

        Args:
            id (str): Cart ID.

        Returns:
            Response: JSON response with delete status and HTTP status code.
        """
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code
    
class ReceiptsAPI(MethodView):
    """
    API endpoint for managing receipts.

    Provides GET, POST, PUT, and DELETE methods for receipt data.
    """
    def __init__(self):
        """
        Initialize ReceiptsAPI with option, controller, and cache keys.
        """
        self.option = "receipts"
        self.api_transaction = ApiControllerTransactions(option=self.option)
        self.cache_keys = cache_key_mapper.get(self.option)

    @role_required(["administrator", "client"])
    def get(self, id=None):
        """
        Retrieve receipt(s).

        Args:
            id (str, optional): Receipt ID. If not provided, returns all receipts.

        Returns:
            Response: JSON response with receipt data and HTTP status code.
        """
        cache_key = f"{self.cache_keys[1]}_{id}" if id else self.cache_keys[0]
        data, http_code = self.api_transaction._get(id, cache_key)
        return jsonify(data), http_code

    @role_required(["administrator"])
    @reject_fields("status", "id", "last_modified", "receipt_number")
    def post(self):
        """
        Create a new receipt.

        Returns:
            Response: JSON response with creation status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._post(request_data)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    @reject_fields("id", "last_modified", "receipt_number", "cart_id",
                   "sale_id", "total_amount")
    def put(self, id):
        """
        Update an existing receipt.

        Args:
            id (str): Receipt ID.

        Returns:
            Response: JSON response with update status and HTTP status code.
        """
        request_data = request.json
        msg, http_code = self.api_transaction._put(request_data, id, self.cache_keys)
        return jsonify(msg), http_code

    @role_required(["administrator"])
    def delete(self, id):
        """
        Delete a receipt.

        Args:
            id (str): Receipt ID.

        Returns:
            Response: JSON response with delete status and HTTP status code.
        """
        msg, http_code = self.api_transaction._delete(id, self.cache_keys)
        return jsonify(msg), http_code