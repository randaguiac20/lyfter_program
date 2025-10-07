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

# Backup directory
BACKUP_DIR = "db_backups"

# Table keys
user_fields = ["id", "first_name", "last_name", "email", "username", "account_status", "birthday"]
car_fields = ["id", "brand", "model", "manufactured_year", "state", "status"]
rentacar_fields = ["id", "user_id", "car_id", "rent_date", "return_date", "status"]
