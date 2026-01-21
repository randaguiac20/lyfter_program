"""main.py

Main entry point for the Fruit Products REST API application.
Initializes the Flask app, configures extensions, creates database manager,
registers all API endpoints, and runs the server with HTTPS.
"""

from modules.db_manager import DBManager
from modules.jwt_manager import JWT_Manager
from flask import Flask, Blueprint
from modules.config import CACHE_TYPE, CACHE_DEFAULT_TIMEOUT, DEFAULT_ADMIN
from modules.https_config import ssl_context
from modules.cache_config import cache
from repositories.user_repository import UserRepository
from repositories.registration_repository import RegistrationRepository
from repositories.login_repository import LoginRepository
from repositories.refresh_token_repository import RefreshTokenRepository
from repositories.address_repository import AddressRepository
from repositories.product_repository import ProductRepository
from repositories.shoppping_cart_repository import ShoppingCartRepository
from repositories.receipt_repository import ReceiptRepository
from repositories.shoppping_cart_product_repository import ShoppingCartProductRepository
from repositories.buy_fruits_repository import BuyFruitRepository
from modules.secret_keys import generate_private_key, password_hash
from modules.models import _models
from modules.config import FILE_PATH



def write_token(token):
    """
    Write an authentication token to a file.
    
    Args:
        token (str): The JWT token to write to file.
    """
    with open(f'{FILE_PATH}/token', 'w') as f:
        f.write(token)

def register_api(app, name, db_manager):
    """
    Registers all API endpoints with the Flask app.

    Args:
        app (Flask): The Flask application instance.
        name (str): The base path for all endpoints (e.g., 'fruit_products').
        db_manager (DB_Manager): Database manager instance.

    Returns:
        None
    """
    # Token refresh endpoint
    refresh_token_repo = RefreshTokenRepository.as_view("refresh-token", db_manager)
    app.add_url_rule(f"/{name}/refresh-token", view_func=refresh_token_repo, methods=["POST"])

    # login and me endpoints
    login_repo = LoginRepository.as_view("login", db_manager)
    app.add_url_rule(f"/{name}/login", view_func=login_repo, methods=["POST"])
    app.add_url_rule(f"/{name}/me", view_func=login_repo, methods=["GET"])

    # register users endpoints
    register_repo = RegistrationRepository.as_view("register", db_manager)
    app.add_url_rule(f"/{name}/register", view_func=register_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/register/<id>", view_func=register_repo, methods=["GET", "PUT", "DELETE"])

    # users endpoints
    user_repo = UserRepository.as_view("users", db_manager)
    app.add_url_rule(f"/{name}/users", view_func=user_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/users/<id>", view_func=user_repo, methods=["GET", "PUT", "DELETE"])

    # address endpoints
    address_repo = AddressRepository.as_view("addresses", db_manager)
    app.add_url_rule(f"/{name}/addresses", view_func=address_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/addresses/<id>", view_func=address_repo, methods=["GET", "PUT", "DELETE"])

    # product endpoints
    product_repo = ProductRepository.as_view("products", db_manager)
    app.add_url_rule(f"/{name}/products", view_func=product_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/products/<id>", view_func=product_repo, methods=["GET", "PUT", "DELETE"])

    # shopping cart endpoints
    shoping_cart_repo = ShoppingCartRepository.as_view("shopping_carts", db_manager)
    app.add_url_rule(f"/{name}/shopping_carts", view_func=shoping_cart_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/shopping_carts/<id>", view_func=shoping_cart_repo, methods=["GET", "PUT", "DELETE"])

    # receipt endpoints
    receipt_repo = ReceiptRepository.as_view("receipts", db_manager)
    app.add_url_rule(f"/{name}/receipts", view_func=receipt_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/receipts/<id>", view_func=receipt_repo, methods=["GET", "PUT", "DELETE"])

    # shopping cart product endpoints
    shoping_cart_product_repo = ShoppingCartProductRepository.as_view("shopping_cart_products", db_manager)
    app.add_url_rule(f"/{name}/shopping_cart_products", view_func=shoping_cart_product_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/shopping_cart_products/<id>", view_func=shoping_cart_product_repo, methods=["GET", "PUT", "DELETE"])

    # buy fruits endpoints
    buy_fruit_repo = BuyFruitRepository.as_view("buy-fruits", db_manager)
    app.add_url_rule(f"/{name}/buy-fruits", view_func=buy_fruit_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/buy-fruits/<id>", view_func=buy_fruit_repo, methods=["GET", "PUT", "DELETE"])



if __name__ == '__main__':
    """
    Main entry point for the application.
    Initializes the Flask app, configures extensions, creates database manager,
    registers all API endpoints, sets up session teardown, and runs the server with SSL.
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Generate keys
    generate_private_key()

    # Configure cache
    app.config['CACHE_TYPE'] = CACHE_TYPE
    app.config['CACHE_DEFAULT_TIMEOUT'] = CACHE_DEFAULT_TIMEOUT
    cache.init_app(app)
    
    # Initialize database manager
    db_manager = DBManager()
    db_manager.drop_tables()
    db_manager.create_tables()
    db_manager._get_model_name("register_user")

    # CRITICAL: Register teardown handler for session cleanup
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """
        Automatically close database sessions after each request.
        This runs whether the request succeeded or raised an exception.
        
        Args:
            exception: Any exception that occurred during the request (or None)
        """
        db_manager.remove_session()
    
    # Create Admin User
    session = db_manager.sessionlocal()
    try:
        model_class = db_manager._get_model()
        password = password_hash(DEFAULT_ADMIN)
        data = {"email": "admin@administrator.com",
                "password": f"{password}", "role": "administrator"}
        new_record = model_class(**data)
        db_manager.insert(session, new_record)
    finally:
        session.close()

    # Create token
    jwt = JWT_Manager()
    token = jwt.encode(data)
    write_token(token)

    # Register all API endpoints
    register_api(app, "fruit_products", db_manager)
    
    # Run the application with SSL
    app.run(
        ssl_context=ssl_context,
        host="localhost",
        port=5001,
        debug=True
    )