from functools import wraps
import jwt
from flask import request, jsonify
import logging
from modules.config import FILE_PATH

# Read keys
def read_keys():
    with open(f'{FILE_PATH}/private.pem', 'rb') as f:
        private_key = f.read()

    with open(f'{FILE_PATH}/public.pem', 'rb') as f:
        public_key = f.read()

    return private_key,public_key


class JWT_Manager:
    def __init__(self, secret=None, algorithm="RS256"):
        self.private_key = read_keys()[0]
        self.public_key = read_keys()[1]
        self.secret = secret
        self.algorithm = algorithm if self.secret is None else "HS256"

    def encode(self, data):
        try:
            if self.secret:
                encoded = jwt.encode(data, self.secret, algorithm=self.algorithm)
                return encoded
            encoded = jwt.encode(data, self.private_key, algorithm=self.algorithm)
            return encoded
        except Exception as e:
            print(e)
            return None

    def decode(self, token):
        try:
            if self.secret:
                decoded = jwt.decode(token, self.secret, algorithms=[self.algorithm])
                return decoded
            decoded = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            return decoded
        except Exception as e:
            print(e)
            return None


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def require_jwt(required_roles=None):
    """
    Usage:
        @require_jwt()                              # Any user
        @require_jwt("admin")                       # Single role
        @require_jwt(["admin", "moderator"])        # Multiple roles
    """
    def actual_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            PUBLIC_KEY = read_keys()[1]
            
            if not token:
                logger.warning("No token provided")
                return jsonify({"error": "No token provided"}), 401
            
            try:
                payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
                user_role = payload.get('role')
                ALLOWED_ROLES = ["client", "administrator"]
                # Check role if required
                if required_roles and user_role in ALLOWED_ROLES:
                    # Convert single string to list
                    roles = [required_roles] if isinstance(required_roles, str) else required_roles
                    
                    if user_role not in roles:
                        logger.warning(f"User {payload.get('id')} with role '{user_role}' attempted to access resource requiring roles: {roles}")
                        return jsonify({"error": f"Access denied. Required role: {', '.join(roles)}"}), 403
                
                logger.info(f"User {payload.get('id')} (role: {user_role}) authenticated")
                
                request.user_id = payload.get('id')
                request.user_role = user_role
                
                return f(*args, **kwargs)
                
            except jwt.ExpiredSignatureError:
                logger.error("Token expired")
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError as e:
                logger.error(f"Invalid token: {str(e)}")
                return jsonify({"error": "Invalid token"}), 401
        
        return decorated_function
    return actual_decorator