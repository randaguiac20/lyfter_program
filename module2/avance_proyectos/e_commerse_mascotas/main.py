"""
main.py

Entry point for the E-Commerce Mascotas API application.
Initializes the Flask app, configures extensions, sets up the database and admin user,
registers all API endpoints, and runs the server with SSL.

Modules imported:
    - Flask and related extensions
    - API endpoint classes for registration, products, users, sales, inventory, and login
    - Data manager for database operations
    - Configuration modules for cache, authentication, and SSL
"""

from flask import Flask
from api.registration import UserRegistration, ProductRegistration
from api.products import ProductAPI
from api.users import UsersAPI
from api.sales import CartsAPI, SalesAPI, ReceiptsAPI
from api.inventory import InventoryAPI
from api.login import LoginAPI
from data_manager.db_connector import DataManager as dm
from configurations.config import CACHE_TYPE, CACHE_DEFAULT_TIMEOUT
from configurations.https_config import ssl_context
from configurations.cache_config import cache
from configurations.auth_config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, jwt
from flask import Blueprint


def register_api(app, name):
    """
    Registers all API endpoints with the Flask app.

    Args:
        app (Flask): The Flask application instance.
        name (str): The base path for all endpoints (e.g., 'pet_shop').

    Returns:
        None
    """
    # login endpoint
    login_api = LoginAPI.as_view("login_api")
    app.add_url_rule(f"/{name}/login", view_func=login_api)
    
    # user_registration
    user_registration = UserRegistration.as_view("user_registration")
    app.add_url_rule(f"/{name}/user_registration", view_func=user_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/user_registration/<id>", view_func=user_registration, methods=["GET", "PUT", "DELETE"])
    
    # product_registration
    product_registration = ProductRegistration.as_view("product_registration")
    app.add_url_rule(f"/{name}/product_registration", view_func=product_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/product_registration/<id>", view_func=product_registration, methods=["GET", "PUT", "DELETE"])

    # product
    products = ProductAPI.as_view("products")
    app.add_url_rule(f"/{name}/products", view_func=products, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/products/<id>", view_func=products, methods=["GET", "PUT", "DELETE"])
    
    # users
    users = UsersAPI.as_view("users")
    app.add_url_rule(f"/{name}/users", view_func=users, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/users/<id>", view_func=users, methods=["GET", "PUT", "DELETE"])
    
    # carts
    carts = CartsAPI.as_view("carts")
    app.add_url_rule(f"/{name}/carts", view_func=carts, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/carts/<id>", view_func=carts, methods=["GET", "PUT", "DELETE"])
    
    # sales
    sales = SalesAPI.as_view("sales")
    app.add_url_rule(f"/{name}/sales", view_func=sales, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/sales/<id>", view_func=sales, methods=["GET", "PUT", "DELETE"])

    # receipts
    receipts = ReceiptsAPI.as_view("receipts")
    app.add_url_rule(f"/{name}/receipts", view_func=receipts, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/receipts/<id>", view_func=receipts, methods=["GET", "PUT", "DELETE"])

    # inventory
    inventory = InventoryAPI.as_view("inventory")
    app.add_url_rule(f"/{name}/inventory", view_func=inventory, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/inventory/<id>", view_func=inventory, methods=["GET", "PUT", "DELETE"])


if __name__ == "__main__":
    """
    Main entry point for the application.
    Initializes the Flask app, configures extensions, creates necessary directories and admin user,
    registers all API endpoints, and runs the server with SSL.
    """
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = CACHE_TYPE
    app.config['CACHE_DEFAULT_TIMEOUT'] = CACHE_DEFAULT_TIMEOUT
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    jwt.init_app(app)
    cache.init_app(app)
    data_manager = dm()
    data_manager.query_file.create_directories()
    data_manager.create_admin_data()
    register_api(app, "pet_shop")
    app.run(ssl_context=ssl_context, host="0.0.0.0",
            port=5001, debug=True)