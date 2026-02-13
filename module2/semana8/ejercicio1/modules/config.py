"""config.py

Application configuration module containing database settings, authentication
configuration, caching options, and file paths for the Fruit Products API.

Constants:
    DB_NAME: PostgreSQL database name.
    DB_USERNAME: Database username.
    DB_PASSWORD: Database password.
    DB_HOST: Database host address.
    DB_PORT: Database port number.
    SCHEMA: Database schema name.
    ALLOWED_ROLES: List of valid user roles.
    DEFAULT_ADMIN: Default administrator password.
    CACHE_TYPE: Flask-Caching backend type.
    CACHE_DEFAULT_TIMEOUT: Cache timeout in seconds.
    CERTS_DIR: Directory for SSL certificates.
    FILE_PATH: Directory for secret keys and tokens.
"""

import os
from sqlalchemy.orm import (declarative_base)
from sqlalchemy import MetaData
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# Now use os.getenv() to read the variables
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
SCHEMA = os.getenv("SCHEMA")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")  # Note: You have REDIS_HOST twice in .env
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Roles
ALLOWED_ROLES = ["client", "administrator"]

# SCHEMA and ORM Base
_metadata = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=_metadata)

# DEFAULT ADMIN
DEFAULT_ADMIN = os.getenv("DEFAULT_ADMIN")

# Cache settings for Flask-Caching
CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for file-based or memory-based caching
CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

# Cert directory
ROOT_DIR = os.getcwd()
CERTS_DIR = f"{ROOT_DIR}/certs"

# KEYs
FILE_PATH = os.getenv("FILE_PATH")
