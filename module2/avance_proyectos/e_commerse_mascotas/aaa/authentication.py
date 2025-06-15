from werkzeug.security import generate_password_hash, check_password_hash

def generate_password(data):
    """
    Generate a hashed password for a user.

    Args:
        data (dict): User data containing 'lastname' and 'name'.

    Returns:
        str: Hashed password.
    """
    password = f"{data.get('lastname')}#{data.get('name')}.2025"
    return generate_password_hash(password)

def check_password(user_password, request_password):
    """
    Check if the provided password matches the stored hash.

    Args:
        user_password (str): Hashed password from the database.
        request_password (str): Password provided by the user.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return check_password_hash(user_password, request_password)