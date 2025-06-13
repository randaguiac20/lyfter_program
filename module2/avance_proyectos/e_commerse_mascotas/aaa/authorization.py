from flask_jwt_extended import (jwt_required, get_jwt)
from flask import jsonify
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict access to endpoints based on user roles.

    Args:
        allowed_roles (list): List of allowed roles.

    Returns:
        function: Decorated function with role-based access control.
    """
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role not in allowed_roles:
                return jsonify({"msg": "Forbidden - insufficient role"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator