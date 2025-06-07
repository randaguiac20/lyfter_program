from werkzeug.security import generate_password_hash, check_password_hash



def generate_password(data):
    password = f"{data.get("lastname")}#{data.get("name")}.2025"
    return generate_password_hash(password)

def check_password(user_password, request_password):
    return check_password_hash(user_password, request_password)

