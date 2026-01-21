"""
https_config.py

Handles SSL certificate generation and configuration for running the Flask app with HTTPS.
Creates a development certificate if it does not exist and sets the SSL context for the server.
"""

from werkzeug.serving import make_ssl_devcert
from modules.config import CERTS_DIR
import os

# Ensure the certificates directory exists
os.makedirs(CERTS_DIR, exist_ok=True)

# Path for the development certificate (without extension)
CERT_FILE = os.path.join(CERTS_DIR, "dev")

# Generate a self-signed development certificate for localhost if not present
make_ssl_devcert(CERT_FILE, host='localhost')

# SSL context tuple (certificate file, key file) for Flask app
ssl_context = (os.path.join(CERTS_DIR, "dev.crt"), os.path.join(CERTS_DIR, "dev.key"))