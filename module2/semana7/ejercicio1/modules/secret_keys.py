"""secret_keys.py

Cryptographic key generation and password hashing utilities.
Handles RSA key pair generation for JWT tokens and secure password operations.
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from werkzeug.security import generate_password_hash, check_password_hash
from modules.config import FILE_PATH


def generate_private_key():
    """
    Generate an RSA private key and save it to a PEM file.
    
    Creates a 2048-bit RSA private key and saves it to the secrets directory.
    Also triggers public key generation.
    """
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


def generate_public_key(private_key):
    """
    Generate a public key from a private key and save it to a PEM file.
    
    Args:
        private_key: RSA private key object.
    """
    public_key = private_key.public_key()

    # Save public key to file
    with open(f'{FILE_PATH}/public.pem', 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def password_hash(password):
    """
    Hash a password using PBKDF2 with SHA-256.
    
    Args:
        password (str): Plain text password to hash.
        
    Returns:
        str: Hashed password string.
    """
    hashed = generate_password_hash(password, method='pbkdf2:sha256')
    return hashed


def verify_password(hashed, password):
    """
    Verify a password against its hash.
    
    Args:
        hashed (str): The hashed password to check against.
        password (str): Plain text password to verify.
        
    Returns:
        bool: True if password matches, False otherwise.
    """
    is_valid = check_password_hash(hashed, password)
    return is_valid