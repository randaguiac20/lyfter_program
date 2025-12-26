from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from werkzeug.security import generate_password_hash, check_password_hash
from modules.config import FILE_PATH


# Generate private key
def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Save private key to file
    with open(f'{FILE_PATH}/private.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    generate_public_key(private_key)

# Generate public key from private key
def generate_public_key(private_key):
    public_key = private_key.public_key()

    # Save public key to file
    with open(f'{FILE_PATH}/public.pem', 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def password_hash(password):
    hashed = generate_password_hash(password, method='pbkdf2:sha256')
    return hashed

# Verify a password
def verify_password(hashed, password):
    is_valid = check_password_hash(hashed, password)
    return is_valid