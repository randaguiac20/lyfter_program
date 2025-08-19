import os

DB_NAME = "lyfter"
DB_USERNAME = "randall_aguilar"
DB_PASSWORD = "lyfter_password"
DB_HOST = "localhost"
DB_PORT = "5450"
SQL_FILE = "database/schema.sql"

# Cache settings for Flask-Caching
CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for file-based or memory-based caching
CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

# Cert directory
ROOT_DIR = os.getcwd()
CERTS_DIR = f"{ROOT_DIR}/certs"

# User repo queries
user_repo_queries = {
    "GET_ALL": "SELECT * FROM lyfter_car_rental.users;",
    "GET_USER_BY_ID": "SELECT * FROM lyfter_car_rental.users WHERE id = (%s);"
}
