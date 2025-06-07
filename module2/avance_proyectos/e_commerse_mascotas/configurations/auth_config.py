from datetime import timedelta
from flask_jwt_extended import JWTManager

# JWT Manager
jwt = JWTManager()

# Secrects
JWT_SECRET_KEY = "pet_super_secret_key"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

