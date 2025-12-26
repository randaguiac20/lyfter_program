import os
from sqlalchemy.orm import (declarative_base)
from sqlalchemy import MetaData


# DB options
DB_NAME = "lyfter_7_week"
DB_USERNAME = "randall_aguilar"
DB_PASSWORD = "lyfter_password"
DB_HOST = "localhost"
DB_PORT = "5452"
SQL_FILE = "database/schema.sql"
SCHEMA = "lyfter_week_7"

# SCHEMA and ORM Base
_metadata = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=_metadata)

# SECRETS
secret = "trespatitos"
secret_algorithm = "RS256"

# Cache settings for Flask-Caching
CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for file-based or memory-based caching
CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

# Cert directory
ROOT_DIR = os.getcwd()
CERTS_DIR = f"{ROOT_DIR}/certs"
