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


# DB options
DB_NAME = "lyfter_7_week"
DB_USERNAME = "randall_aguilar"
DB_PASSWORD = "lyfter_password"
DB_HOST = "localhost"
DB_PORT = "5452"
SQL_FILE = "database/schema.sql"
SCHEMA = "lyfter_week_7"

# Roles
ALLOWED_ROLES = ["client", "administrator"]

# SCHEMA and ORM Base
_metadata = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=_metadata)

# DEFAULT ADMIN
DEFAULT_ADMIN = "Just0n3Adm1inP455word"

# Cache settings for Flask-Caching
CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for file-based or memory-based caching
CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

# Cert directory
ROOT_DIR = os.getcwd()
CERTS_DIR = f"{ROOT_DIR}/certs"

# KEYs
FILE_PATH = "/Users/Randall_Aguilar/projects/personal/git/lyfter_program/module2/semana7/ejercicio1/secrets"
