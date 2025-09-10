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

from flask import Flask, Blueprint
from modules.repositories import (UserRepository, CarRepository,
                                  RentCarUsers)
from modules.config import CACHE_TYPE, CACHE_DEFAULT_TIMEOUT
from modules.https_config import ssl_context
from modules.cache_config import cache
from modules.db_manager import db_manager


def register_api(app, name, db_manager):
    """
    Registers all API endpoints with the Flask app.

    Args:
        app (Flask): The Flask application instance.
        name (str): The base path for all endpoints (e.g., 'pet_shop').

    Returns:
        None
    """
    
    # users
    user_repo = UserRepository.as_view("users", db_manager)
    app.add_url_rule(f"/{name}/users", view_func=user_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/users/<option>", view_func=user_repo, methods=["GET", "PUT", "DELETE"])

    # cars
    car_repo = CarRepository.as_view("cars", db_manager)
    app.add_url_rule(f"/{name}/cars", view_func=car_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/cars/<option>", view_func=car_repo, methods=["GET", "PUT", "DELETE"])

    # rent cars
    rentcars_repo = RentCarUsers.as_view("rentcars", db_manager)
    app.add_url_rule(f"/{name}/rentcars", view_func=rentcars_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/rentcars/<option>", view_func=rentcars_repo, methods=["GET", "PUT", "DELETE"])


if __name__ == "__main__":
    """
    Main entry point for the application.
    Initializes the Flask app, configures extensions, creates necessary directories and admin user,
    registers all API endpoints, and runs the server with SSL.
    """
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = CACHE_TYPE
    app.config['CACHE_DEFAULT_TIMEOUT'] = CACHE_DEFAULT_TIMEOUT
    cache.init_app(app)
    manager = db_manager()
    manager.initialize_schema()
    manager.create_database_if_not_exists()
    register_api(app, "lyfter_car_rental", manager)
    app.run(ssl_context=ssl_context, host="0.0.0.0",
            port=5001, debug=True)