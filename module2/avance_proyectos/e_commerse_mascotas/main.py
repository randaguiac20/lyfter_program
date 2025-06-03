from file_manager import (FileTransactions)
from flask import Flask
from cache_config import cache
from users import UserRegistration
from products import ProductRegistration



def register_api(app, name):
    user_registration = UserRegistration.as_view(f"user_registration")
    product_registration = ProductRegistration.as_view(f"product_registration")

    # user_registration
    app.add_url_rule(f"/{name}/user_registration", view_func=user_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/user_registration/<user_id>", view_func=user_registration, methods=["GET"])
    app.add_url_rule(f"/{name}/user_registration/<user_id>", view_func=user_registration, methods=["PUT", "DELETE"])
    
    # product_registration
    app.add_url_rule(f"/{name}/product_registration", view_func=product_registration, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/product_registration/<product_id>", view_func=product_registration, methods=["GET"])
    app.add_url_rule(f"/{name}/product_registration/<product_id>", view_func=product_registration, methods=["PUT", "DELETE"])


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = 'SimpleCache'  # Use SimpleCache for file-based or memory-based
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    cache.init_app(app)
    file_transaction = FileTransactions()
    file_transaction.create_directories()
    register_api(app, "pet_shop")
    app.run(host="0.0.0.0", port=5001, debug=True)