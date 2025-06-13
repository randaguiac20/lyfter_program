"""
controller.py

Provides controller classes for handling API transactions for various endpoints,
including login, CRUD operations, and complex business logic for carts, receipts,
sales, and inventory. Handles schema validation, caching, and data persistence.
"""

from flask import request
from validators.schema_validator import schema_validator
from data_manager.db_connector import DataManager
from configurations.config import directory_mapper
from configurations.cache_config import cache, cache_key_mapper
from validators.validator import content_mapper
from aaa.authentication import generate_password, check_password
from datetime import datetime
import uuid
from flask_jwt_extended import create_access_token


class LoginAPITransactions:
    """
    Handles login-related API transactions, including authentication and token generation.
    """

    def __init__(self, option):
        """
        Initialize LoginAPITransactions.

        Args:
            option (str): The entity type (e.g., 'users').
        """
        self.option = option
        self.schema = schema_validator
        self.db = DataManager()
        self.directory = directory_mapper.get(option)
    
    def _post(self, data):
        """
        Authenticate a user and generate a JWT access token.

        Args:
            data (dict): Login data containing 'email' and 'password'.

        Returns:
            tuple: (dict, int) Response message and HTTP status code.
        """
        dir_path = self.directory
        email = data.get("email")
        password = data.get("password")
        user_data, http_code = self.db.get_data_by_email(dir_path, email)
        
        if http_code == 400:
            return {"msg": "User is disabled."}, 400
        if not user_data or not check_password(user_data.get("password"), password):
            return {"msg": "Invalid email or password"}, 401
        schema_true, msg = self.schema(self.option, user_data)
        if schema_true is False:
            return msg, 400
        token = create_access_token(identity=email, additional_claims={"role": user_data.get("role")})
        return {"access_token": token}, 200

class ApiControllerTransactions:
    """
    Handles CRUD operations and business logic for API endpoints.

    Supports GET, POST, PUT, DELETE, and complex updates for carts, receipts, sales, and inventory.
    """

    def __init__(self, option):
        """
        Initialize ApiControllerTransactions.

        Args:
            option (str): The entity type (e.g., 'users', 'products').
        """
        self.schema = schema_validator
        self.db = DataManager()
        self.directory_mapper = directory_mapper
        self.directory = directory_mapper.get(option)
        self.option = option
        self.content_mapper = content_mapper
        self.cache = cache
        self.cache_key_mapper = cache_key_mapper

    def _get(self, id, cache_key):
        """
        Retrieve one or more items from the data store, with caching.

        Args:
            id (str or None): Item ID. If None, retrieves all items.
            cache_key (str): Cache key for the item(s).

        Returns:
            tuple: (data, int) Data and HTTP status code.
        """
        _data = self.cache.get(cache_key)
        if id:
            if _data:
                return _data, 200
            file_id = f"{self.directory}/{id}.json"
            data, http_code = self.db.get_data_item(file_id)
            if http_code == 200:
                self.cache.set(cache_key, data)
            return data, http_code
        data, http_code = self.db.get_data_items(self.directory)
        if _data is None:
            self.cache.set(cache_key, data)
        else:
            data = _data
        filter_status = request.headers.get("status")
        if filter_status:
            data = list(
                filter(lambda _status: _status["status"] == filter_status, data)
            )
        return data, http_code
    
    def _post(self, request_data):
        """
        Create a new item in the data store, handling special logic for certain entities.

        Args:
            request_data (dict): Data for the new item.

        Returns:
            tuple: (dict, int) Response message and HTTP status code.
        """
        dir_path = self.directory
        if self.option == "carts":
            request_data['receipt_id'] = str(uuid.uuid4())
            request_data['sale_id'] = str(uuid.uuid4())
            request_data['status'] = "completed" if request_data['checkout'] == "True" else "in_progress"
        if self.option == "product_registration":
            request_data['product_id'] = str(uuid.uuid4())
            request_data['inventory_id'] = str(uuid.uuid4())
            request_data['status'] = "registered"
        if self.option == "user_registration":
            request_data['user_id'] = str(uuid.uuid4())
            request_data['password'] = generate_password(request_data)
            request_data['status'] = "registered"
        request_data['id'] = str(uuid.uuid4())
        request_data['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        schema_true, msg = self.schema(self.option, request_data)
        if schema_true is False:
            return msg, 400
        file_id = request_data.get('id')
        filename = f"{self.directory}/{file_id}.json"
        msg, http_code = self.db.save_data(request_data=request_data, filepath=filename,
                                           directory_path=dir_path, option=self.option)
        if self.option == "carts":
            rfile_id = request_data.get('receipt_id')
            rcache_keys = self.cache_key_mapper.get("receipts")
            rmsg, rhttp_code = self._update_cart_dependencies(_request_data=request_data, id=rfile_id,
                                                              cache_keys=rcache_keys, option="receipts")
            if rhttp_code != 200:
                return rmsg, rhttp_code
            sfile_id = request_data.get('sale_id')
            scache_keys = self.cache_key_mapper.get("sales")
            smsg, shttp_code = self._update_cart_dependencies(_request_data=request_data, id=sfile_id,
                                                              cache_keys=scache_keys, option="sales")
            if shttp_code != 200:
                return smsg, shttp_code
        return msg, http_code

    def _put(self, request_data, id, cache_keys, dir_path=None, option=None):
        """
        Update an existing item in the data store.

        Args:
            request_data (dict): Updated data.
            id (str): Item ID.
            cache_keys (list): List of cache keys to invalidate.
            dir_path (str, optional): Directory path override.
            option (str, optional): Entity type override.

        Returns:
            tuple: (str, int) Response message and HTTP status code.
        """
        dir_path = self.directory if option is None else dir_path
        option = self.option if option is None else option
        file_id = f"{dir_path}/{id}.json"
        data, http_code = self.db.get_data_item(file_id)
        request_data['last_modified'] = datetime.now().strftime("%d_%m_%Y-%H:%M")
        try:
            data.update(request_data)
        except AttributeError:
            msg = f"{option} {id} was not found."
            return msg, 404
        schema_true, msg = self.schema(option, data)
        if schema_true is False:
            return msg, 400
        db_true_false, data = self.db.update_data(data, file_id)
        if db_true_false is False:
            msg = f"{option} {data.get('id')} was not updated."
            return msg, 404
        schema_true, msg = self.schema(option, data)
        if schema_true is False:
            return msg, 400
        msg = f"{option} {data.get('id')} was updated."
        # Invalidate caches
        self.cache.delete(cache_keys[0])
        self.cache.delete(f"{cache_keys[1]}_{id}")
        return msg, 200
    
    def _update_cart_dependencies(self, _request_data, id, cache_keys, option=None):
        """
        Update related entities when a cart is updated (e.g., receipts, sales, inventory).

        Args:
            _request_data (dict): Data for the cart update.
            id (str): Cart ID.
            cache_keys (list): List of cache keys to invalidate.
            option (str, optional): Entity type override.

        Returns:
            tuple: (str or dict, int) Response message and HTTP status code.
        """
        checkout_option = _request_data.get("checkout")
        receipts_dir_path = self.directory_mapper.get("receipts")
        receipts_cache_keys = self.cache_key_mapper.get("receipts")
        sales_dir_path = self.directory_mapper.get("sales")
        sales_cache_keys = self.cache_key_mapper.get("sales")
        inventory_dir_path = self.directory_mapper.get("inventory")
        inventory_cache_keys = self.cache_key_mapper.get("inventory")
        cart_dir_path = self.directory_mapper.get("carts")
        cart_cache_keys = self.cache_key_mapper.get("carts")
        if option is None:
            cart_file_id = f"{cart_dir_path}/{id}.json"
            cart_data, http_code = self.db.get_data_item(cart_file_id)
            if http_code != 200:
                msg = f"File id {id} was not found"
                return msg, 404
            request_data = cart_data | _request_data
        if option:
            request_data = _request_data
        receipt_id = request_data.get("receipt_id")
        receipt_file_id = f"{receipts_dir_path}/{receipt_id}.json"
        receipt_data, rhttp_code = self.db.get_data_item(receipt_file_id)
        if rhttp_code != 200:
            rmsg = {"message": f"Receipt ID {receipt_id} not found."}
            return rmsg, rhttp_code
        cart_id = request_data.get("id")
        sale_id = request_data.get("sale_id")
        sale_file_id = f"{sales_dir_path}/{sale_id}.json"
        products = request_data.get("products")
        data_inventory, _ = self.db.get_data_items(inventory_dir_path)
        total_amount = float()
        for data in data_inventory:
            for product in products:
                if data.get("code") == product.get("code"):
                    print(f"data: {data.get('code')} - product: {product.get('code')}")
                    if data.get("quantity") >= product.get("quantity"):
                        # Update cart status
                        cart_status = {
                            "True": "completed",
                            "False": "in_progress"
                        }
                        request_data["status"] = cart_status.get(checkout_option)
                        cschema_true, cmsg = self.schema("carts", request_data)
                        if cschema_true is False:
                            return cmsg, 400
                        cdata, chttp_code = self._put(request_data, cart_id, cart_cache_keys,
                                                     dir_path=cart_dir_path, option="carts")
                        if chttp_code != 200:
                            return cmsg, chttp_code
                        # Update receipt total amount
                        update_amount = {
                            "True": product.get("quantity") * data.get("price"),
                            "False": 0
                        }
                        amount = update_amount.get(checkout_option)
                        total_amount += amount
                        receipt_data["products"] = [{**_product, **product} if _product.get("code") == product.get("code") else _product
                                                    for index, _product in enumerate(receipt_data.get("products", []))]
                        # Update sale status
                        sdata, shttp_code = self.db.get_data_item(sale_file_id)
                        if shttp_code != 200:
                            smsg = {"message": f"Sale ID {sale_id} not found."}
                            return smsg, shttp_code
                        payment_update = {
                            "True": "completed_payment",
                            "False": "pending_payment"
                        }
                        sdata["status"] = payment_update.get(checkout_option)
                        sschema_true, smsg = self.schema("sales", sdata)
                        if sschema_true is False:
                            return smsg, 400
                        sdata, shttp_code = self._put(sdata, sale_id, sales_cache_keys,
                                                     dir_path=sales_dir_path, option="sales")
                        if shttp_code != 200:
                            return ssmg, shttp_code
                        # Update inventory
                        quantity = {
                            "True": data.get("quantity") - product.get("quantity"),
                            "False": data.get("quantity") + product.get("quantity")
                        }
                        data["quantity"] = quantity.get(checkout_option)
                        ischema_true, imsg = self.schema("inventory", data)
                        if ischema_true is False:
                            return imsg, 400
                        imsg, ihttp_code = self._put(data, data.get("id"), inventory_cache_keys,
                                                     dir_path=inventory_dir_path, option="inventory")
                        if ihttp_code != 200:
                            return ismg, ihttp_code
                    if data.get("quantity") < product.get("quantity"):
                        msg = {"message": f"No enough products in stock {data.get('name')}"}
                        return msg, 406
                if product.get("code") is None or not "COD_" in product.get("code"):
                    msg = {"message": f"Product does not have the right code."}
                    return msg, 406
        receipt_data["total_amount"] = total_amount
        rschema_true, rmsg = self.schema("receipts", receipt_data)
        if rschema_true is False:
            return rmsg, 400
        receipt_msg, receipt_http_code = self._put(receipt_data, receipt_id, receipts_cache_keys,
                                                   dir_path=receipts_dir_path, option="receipts")
        if receipt_http_code != 200:
            return receipt_msg, receipt_http_code
        msg = f"Updated sales information for receipt id: {receipt_id}"
        return msg, 200

    def _delete(self, id, cache_keys):
        """
        Delete an item from the data store and invalidate caches.

        Args:
            id (str): Item ID.
            cache_keys (list): List of cache keys to invalidate.

        Returns:
            tuple: (str, int) Response message and HTTP status code.
        """
        data = f"{self.directory}/{id}.json"
        msg, http_code = self.db.delete_data(data, self.option)
        # Invalidate caches
        if http_code != 200:
            self.cache.delete(cache_keys[0])
            self.cache.delete(f"{cache_keys[1]}_{id}")
        return msg, http_code