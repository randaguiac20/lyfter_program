from flask_caching import Cache

cache = Cache()


# Cache keys mapper
cache_key_mapper = {
    "user_registration": ["all_users", "user"],
    "product_registration": ["all_products", "product"]
}
