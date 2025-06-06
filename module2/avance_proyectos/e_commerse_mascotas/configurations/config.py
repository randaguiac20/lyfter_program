import os

# ALL Directories require to simulate DB
ROOT_DIR = os.getcwd()
DB_DIR = f"{ROOT_DIR}/db"
REGISTRATIONS_DIR = f"{DB_DIR}/registrations"
USERS_REGISTRATION_DIR = f"{REGISTRATIONS_DIR}/users"
PRODUCT_REGISTRATION_DIR = f"{REGISTRATIONS_DIR}/products"
ROLES_DIR = f"{DB_DIR}/roles"
USERS_DIR = f"{DB_DIR}/users"
INVENTORY_DIR = f"{DB_DIR}/inventory"
SALES_DIR = f"{DB_DIR}/receipts"
PRODUCTS_DIR = f"{DB_DIR}/products"
CERTS_DIR = f"{DB_DIR}/certs"

# List of all directories
directory_list = [
    ROOT_DIR, DB_DIR, REGISTRATIONS_DIR, USERS_REGISTRATION_DIR,
    PRODUCT_REGISTRATION_DIR, ROLES_DIR, USERS_DIR, INVENTORY_DIR,
    SALES_DIR, PRODUCTS_DIR, CERTS_DIR
]

# Directory mapper
directory_mapper = {
    "bd_dir": DB_DIR,
    "user_registration": USERS_REGISTRATION_DIR,
    "product_registration": PRODUCT_REGISTRATION_DIR,
    "role": ROLES_DIR,
    "user": USERS_DIR,
    "inventory": INVENTORY_DIR,
    "sale": SALES_DIR,
    "product": PRODUCTS_DIR,
    "cert": CERTS_DIR
}

# Cache setting use for API Endpoints
CACHE_TYPE = 'SimpleCache'  # Use SimpleCache for file-based or memory-based
CACHE_DEFAULT_TIMEOUT = 300


# BE AWARE OF THAT THIS IS ONLY FOR MOCKING
# PURPOSES OF THIS PROJECT TO SIMULATE A
# DEFAULT USER AND PASSWORD FOR ADMINISTRATION
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

admin_user = {
    "name": "administrator",
    "description": "admin user",
    "email": "administrator@example.com",
    "role": admin_role.get("role"),
    "operations": admin_role.get("operations")
}

# Registration fields set mapper
endpoint_fields_mapper = {
    "user_registration": ["email", "name", "lastname"],
    "product_registration": ["code", "name", "brand"]
}

# Default template for USER, PRODUCT, INVENTORY
default_table_templates = {
    "user": {
        'id': '',
        'email': '',
        'name': '',
        'lastname': '',
        'description': '',
        'last_modified': '',
        'status': ''
        },
    "product": {
        'id': '',
        'code': '',
        'name': '',
        'size': '',
        'breed_size': '',
        'brand': '',
        'price': 0,
        'description': '',
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
        }
}