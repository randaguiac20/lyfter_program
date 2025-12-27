from functools import wraps
import jwt
from flask import request, jsonify
import logging
from datetime import datetime, timedelta
from modules.config import FILE_PATH
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    def encode(self, data, expires_in_minutes: int = 15):
        try:
            payload = data.copy()
            payload['exp'] = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
            payload['iat'] = datetime.utcnow()
            if self.secret:
                encoded = jwt.encode(payload, self.secret, algorithm=self.algorithm)
                return encoded
            encoded = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
            return encoded
        except Exception as e:
            logger.warning(f"Encode token error: {e}")
            return None

    def encode_refresh_token(self, email: str, expires_in_days: int = 30):
        """Generate refresh token with long expiration and minimal data"""
        try:
            payload = {
                'email': email,
                'exp': datetime.utcnow() + timedelta(days=expires_in_days),
                'iat': datetime.utcnow(),
                'type': 'refresh'  # Token type identifier
            }
            if self.secret:
                encoded = jwt.encode(payload, self.secret, algorithm=self.algorithm)
                return encoded
            encoded = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
            return encoded
        except Exception as e:
            logger.warning(f"Encode refresh token error: {e}")
        return None
    
    def decode(self, token):
        try:
            if self.secret:
                decoded = jwt.decode(token, self.secret, algorithms=[self.algorithm])
                return decoded
            decoded = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            return decoded
        except Exception as e:
            logger.warning(f"Decode token error: {e}")
            return None


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
                
                # Check role if required
                if required_roles == user_role:
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