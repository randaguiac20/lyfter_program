from werkzeug.serving import make_ssl_devcert
from configurations.config import CERTS_DIR
import os

os.makedirs(CERTS_DIR, exist_ok=True)
CERT_FILE = os.path.join(CERTS_DIR, "dev")
make_ssl_devcert(CERT_FILE, host='localhost')
ssl_context = (os.path.join(CERTS_DIR, "dev.crt"), os.path.join(CERTS_DIR, "dev.key"))
