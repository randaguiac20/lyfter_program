from modules.db_manager import DB_Manager
from modules.jwt_manager import JWT_Manager
from flask import Flask, Blueprint
from modules.config import CACHE_TYPE, CACHE_DEFAULT_TIMEOUT
from modules.https_config import ssl_context
from modules.cache_config import cache
from modules.user_repository import UserRepository
from modules.registration_repository import RegistrationRepository


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

    # register users endpoints
    register_repo = RegistrationRepository.as_view("register", db_manager)
    app.add_url_rule(f"/{name}/register", view_func=register_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/register/<id>", view_func=register_repo, methods=["GET", "PUT", "DELETE"])

    # users endpoints
    user_repo = UserRepository.as_view("users", db_manager)
    app.add_url_rule(f"/{name}/users", view_func=user_repo, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/users/<id>", view_func=user_repo, methods=["GET", "PUT", "DELETE"])


if __name__ == '__main__':
    """
    Main entry point for the application.
    Initializes the Flask app, configures extensions, creates database manager,
    registers all API endpoints, sets up session teardown, and runs the server with SSL.
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Configure cache
    app.config['CACHE_TYPE'] = CACHE_TYPE
    app.config['CACHE_DEFAULT_TIMEOUT'] = CACHE_DEFAULT_TIMEOUT
    cache.init_app(app)
    
    # Initialize database manager
    db_manager = DB_Manager(drop_table=False)
    
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
    
    # Register all API endpoints
    register_api(app, "fruit_products", db_manager)
    
    # Run the application with SSL
    app.run(
        ssl_context=ssl_context,
        host="localhost",
        port=5001,
        debug=True
    )