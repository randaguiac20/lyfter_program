from flask import Flask
from api.registration import UserRegistration, ProductRegistration
from api.login import LoginAPI
from data_manager.db_connector import DataManager as dm
from configurations.config import CACHE_TYPE, CACHE_DEFAULT_TIMEOUT
from configurations.https_config import ssl_context
from configurations.cache_config import cache
from configurations.auth_config import JWT_SECRET_KEY,JWT_ACCESS_TOKEN_EXPIRES,jwt
from flask import Blueprint



def register_api(app, name):
    # login endpoint
    login_api = LoginAPI.as_view(f"login_api")
    app.add_url_rule(f"/{name}/login", view_func=login_api)
    
    # user_registration
    user_registration = UserRegistration.as_view(f"user_registration")
    app.add_url_rule(f"/{name}/user_registration", view_func=user_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/user_registration/<id>", view_func=user_registration, methods=["GET", "PUT", "DELETE"])
    
    # product_registration
    product_registration = ProductRegistration.as_view(f"product_registration")
    app.add_url_rule(f"/{name}/product_registration", view_func=product_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/product_registration/<id>", view_func=product_registration, methods=["GET", "PUT", "DELETE"])


if __name__ == "__main__":
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
