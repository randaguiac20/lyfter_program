"""
config.py

Configuration module for the E-Commerce Mascotas API.

Defines directory paths for simulating a database using the file system,
cache settings, admin/client roles and users, field mappers, and default
table templates for various entities.
"""

import os

# ALL Directories required to simulate DB
ROOT_DIR = os.getcwd()
DB_DIR = f"{ROOT_DIR}/db"
REGISTRATIONS_DIR = f"{DB_DIR}/registrations"
USERS_REGISTRATION_DIR = f"{REGISTRATIONS_DIR}/users"
PRODUCT_REGISTRATION_DIR = f"{REGISTRATIONS_DIR}/products"
ROLES_DIR = f"{DB_DIR}/roles"
USERS_DIR = f"{DB_DIR}/users"
INVENTORY_DIR = f"{DB_DIR}/inventory"
SALES_DIR = f"{DB_DIR}/sales"
RECEIPTS_DIR = f"{DB_DIR}/receipts"
CARTS_DIR = f"{DB_DIR}/carts"
PRODUCTS_DIR = f"{DB_DIR}/products"
CERTS_DIR = f"{DB_DIR}/certs"

# List of all directories used in the application
directory_list = [
    ROOT_DIR, DB_DIR, REGISTRATIONS_DIR, USERS_REGISTRATION_DIR,
    PRODUCT_REGISTRATION_DIR, ROLES_DIR, USERS_DIR, INVENTORY_DIR,
    SALES_DIR, PRODUCTS_DIR, CERTS_DIR, RECEIPTS_DIR, CARTS_DIR
]

# Directory mapper for quick access to important directories
directory_mapper = {
    "bd_dir": DB_DIR,
    "user_registration": USERS_REGISTRATION_DIR,
    "product_registration": PRODUCT_REGISTRATION_DIR,
    "users": USERS_DIR,
    "inventory": INVENTORY_DIR,
    "sales": SALES_DIR,
    "carts": CARTS_DIR,
    "receipts": RECEIPTS_DIR,
    "products": PRODUCTS_DIR,
    "cert": CERTS_DIR
}

# Cache settings for Flask-Caching
CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for file-based or memory-based caching
CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

# Role definitions for administrator and client
admin_role = {
    "role": "administrator",
    "description": "admin user",
    "operations": ["read", "write", "update", "delete"]
}
client_role = {
    "role": "client",
    "description": "client user",
    "operations": ["read"]
}

# Default admin user configuration
admin_user = {
    "name": "administrator",
    "lastname": "administrator",
    "description": "admin user",
    "email": "administrator@example.com",
    "role": admin_role.get("role"),
    "password": ""
}

# Registration fields set mapper for unique field validation
endpoint_fields_mapper = {
    "inventory": ["name", "size", "breed_size"],
    "sales": ["name", "size", "breed_size"],
    "receipts": ["name", "size", "breed_size"],
    "carts": ["id", "receipt_id", "sale_id"],
    "user_registration": ["email", "name", "lastname"],
    "product_registration": ["code", "name", "brand"]
}

# Default templates for USER, PRODUCT, INVENTORY, RECEIPTS, SALES
default_table_templates = {
    "users": {
        'id': '',
        'email': '',
        'name': '',
        'lastname': '',
        'password': '',
        'role': '',
        'description': '',
        'last_modified': '',
        'status': ''
    },
    "products": {
        'id': '',
        'code': '',
        'name': '',
        'size': '',
        'breed_size': '',
        'brand': '',
        'price': 0,
        'description': '',
        'ingress_date': '',
        'expiration_date': '', 
        'last_modified': '',
        'status': 'disable'
    },
    "inventory": {
        'id': '',
        'code': '',
        'name': '',
        'size': '',
        'breed_size': '',
        'brand': '',
        'quantity': 0,
        'description': '',
        'ingress_date': '',
        'expiration_date': '', 
        'last_modified': '',
        'status': ''
    },
    "receipts": {
        'id': '',
        'receipt_number': '',
        'store_name': 'pet shop',
        'store_email': 'pet_shop@gmail.com',
        'cart_id': '',
        'sale_id': '',
        'products': '',
        'client_email': '',
        'description': '',
        'total_amount': 0,
        'last_modified': ''
    },
    "sales": {
        'id': '',
        'receipt_id': '',
        'cart_id': '',
        'store_name': 'pet shop',
        'store_email': 'pet_shop@gmail.com',
        'client_email': '',
        'description': 'This is your favorite pet shop',
        'last_modified': '',
        'status': 'pending_payment'
    }
}