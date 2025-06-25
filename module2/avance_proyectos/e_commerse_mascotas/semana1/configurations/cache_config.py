"""
cache_config.py

Configuration for Flask-Caching and cache key mapping for different API resources.
Provides a cache instance and a dictionary to map resource names to their cache keys.
"""

from flask_caching import Cache

# Flask-Caching instance for caching API responses
cache = Cache()

# Cache keys mapper
# Maps resource names to a list of cache keys for all items and individual items
cache_key_mapper = {
    "carts": ["all_carts", "carts"],
    "sales": ["all_sales", "sales"],
    "receipts": ["all_receipts", "receipts"],
    "inventory": ["all_inventory", "inventory"],
    "user_registration": ["all_users", "user"],
    "product_registration": ["all_registration_products", "registration_product"],
    "products": ["all_products", "products"],
    "users": ["all_users", "users"]
}