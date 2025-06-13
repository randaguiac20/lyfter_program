"""
auth_config.py

Configuration for JWT authentication, including secret key, token expiration,
and JWTManager initialization for the Flask application.
"""

from datetime import timedelta
from flask_jwt_extended import JWTManager

# JWT Manager instance for handling JWT operations in Flask
jwt = JWTManager()

# Secret key used for encoding JWT tokens
JWT_SECRET_KEY = "pet_super_secret_key"

# Token expiration time (1 hour)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)