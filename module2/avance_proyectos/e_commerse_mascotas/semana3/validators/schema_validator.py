"""
schema_validator.py

Defines Marshmallow schemas for data validation and serialization for the E-Commerce Mascotas API.
Includes custom fields, entity schemas, schema mapping, and utility functions for schema validation
and building new registration datasets.

Classes:
    - StrOrList: Custom Marshmallow field to accept either a string or a list of strings.
    - RoleSchema: Schema for user roles.
    - UserRegistrationSchema: Schema for user registration data.
    - UserSchema: Schema for user data.
    - ProductRegistrationSchema: Schema for product registration data.
    - ProductSchema: Schema for product data.
    - ItemSchema: Schema for product items in carts/receipts.
    - ReceiptSchema: Schema for receipts.
    - SaleSchema: Schema for sales.
    - CartSchema: Schema for carts.
    - InventorySchema: Schema for inventory items.

Functions:
    - schema_validator: Validates data against a schema.
    - schema_builder_for_new_registrations: Builds a dataset for new registrations using a schema.
"""

from marshmallow import (Schema, fields,
                         validate, ValidationError)

class StrOrList(fields.List):
    """
    Custom Marshmallow field that allows a field to accept either a string or a list of strings.
    Converts a string to a single-item list for validation.
    """
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            value = [value]
        elif not isinstance(value, list):
            raise ValidationError("Field should be a string or a list of strings.")
        return super()._deserialize(value, attr, data, **kwargs)

class RoleSchema(Schema):
    """
    Schema for user roles.
    """
    id = fields.Str(required=False)
    role_name = fields.Str(required=True)
    description = fields.Str(required=True)

class UserRegistrationSchema(Schema):
    """
    Schema for user registration data.
    """
    id = fields.UUID(required=False)
    user_id = fields.Str(required=False)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    description = fields.Str(required=False)
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    access_level = StrOrList(fields.Str(required=False, load_default="no_access",
                              validate=validate.OneOf(
                              ["user_registration", "product_registration", "users",
                               "cart", "sales", "products", "inventory", "all", "no_access"])))
    role = fields.Str(required=True,
                      validate=validate.OneOf(
                            ["administrator", 
                             "client"]))
    status = fields.Str(required=False,
                        validate=validate.OneOf(
                            ["registered", 
                             "unregistered"]))

class UserSchema(Schema):
    """
    Schema for user data.
    """
    id = fields.UUID(required=False)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    description = fields.Str(required=False)
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    role = fields.Str(required=True,
                      validate=validate.OneOf(
                            ["administrator", 
                             "client"]))
    status = fields.Str(required=False,
                        validate=validate.OneOf(
                            ["active", 
                             "disable"]))

class ProductRegistrationSchema(Schema):
    """
    Schema for product registration data.
    """
    id = fields.Str(required=False)
    product_id = fields.Str(required=False)
    inventory_id = fields.Str(required=False)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    size = fields.Str(required=True)
    breed_size = fields.Str(required=True)
    brand = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)
    ingress_date = fields.DateTime(required=True, format="%d_%m_%Y")
    expiration_date = fields.DateTime(required=True, format="%d_%m_%Y")
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["registered", 
                             "unregistered"]))

class ProductSchema(Schema):
    """
    Schema for product data.
    """
    id = fields.Str(required=False)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    size = fields.Str(required=True)
    breed_size = fields.Str(required=True)
    brand = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)
    ingress_date = fields.DateTime(required=True, format="%d_%m_%Y")
    expiration_date = fields.DateTime(required=True, format="%d_%m_%Y")
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["active", 
                             "disable"]))

class ItemSchema(Schema):
    """
    Schema for product items in carts and receipts.
    """
    code = fields.Str(required=True)
    quantity = fields.Int(required=False, load_default=0)

class ReceiptSchema(Schema):
    """
    Schema for receipts.
    """
    id = fields.Str(required=False)
    receipt_number = fields.Str(required=True)
    store_name = fields.Str(required=True)
    store_email = fields.Email(required=True)
    cart_id = fields.Str(required=True)
    sale_id = fields.Str(required=True)
    products = fields.List(fields.Nested(ItemSchema), required=True)
    client_email = fields.Str(required=True)
    description = fields.Str(required=True)
    purchase_date = fields.DateTime(required=False, format="%d_%m_%Y-%H:%M")
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    total_amount = fields.Int(required=True)

class SaleSchema(Schema):
    """
    Schema for sales.
    """
    id = fields.Str(required=False)
    receipt_id = fields.Str(required=True)
    cart_id = fields.Str(required=True)
    store_name = fields.Str(required=True)
    store_email = fields.Email(required=True)
    client_email = fields.Str(required=True)
    description = fields.Str(required=True)
    purchase_date = fields.DateTime(required=False, format="%d_%m_%Y-%H:%M")
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["pending_payment", 
                             "completed_payment"]))

class CartSchema(Schema):
    """
    Schema for carts.
    """
    id = fields.Str(required=False)
    receipt_id = fields.Str(required=True)
    sale_id = fields.Str(required=True)
    client_email = fields.Str(required=True)
    products = fields.List(fields.Nested(ItemSchema), required=True)
    description = fields.Str(required=True)
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    checkout = fields.Str(required=False, load_default="False")
    status = fields.Str(required=False, load_default="in_progress",
                        validate=validate.OneOf(
                            ["in_progress", 
                             "completed"]))

class InventorySchema(Schema):
    """
    Schema for inventory items.
    """
    id = fields.Str(required=False)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    size = fields.Str(required=True)
    breed_size = fields.Str(required=True)
    brand = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=False, load_default=0)
    description = fields.Str(required=True)
    ingress_date = fields.DateTime(required=True, format="%d_%m_%Y")
    expiration_date = fields.DateTime(required=True, format="%d_%m_%Y")
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["active", 
                             "disable"]))


# Schema mapper for entity names to Marshmallow schemas
schemas = {
    "roles": RoleSchema,
    "user_registration": UserRegistrationSchema,
    "product_registration": ProductRegistrationSchema,
    "users": UserSchema,
    "products": ProductSchema,
    "sales": SaleSchema,
    "carts": CartSchema,
    "receipts": ReceiptSchema,
    "inventory": InventorySchema
}

def schema_validator(schema, request_data):
    """
    Validate request data against a given schema.

    Args:
        schema (str): Name of the schema/entity.
        request_data (dict): Data to validate.

    Returns:
        tuple: (bool, str) True and "good" if valid, False and error message if not.
    """
    _schema = schemas.get(schema)()
    try:
        _schema.load(request_data)
        msg = "good"
        return True, msg
    except ValidationError as err:
        msg = f"error: Validation failed, messages: {err.messages}"
        return False, msg
    
def schema_builder_for_new_registrations(_schema=None, data_content={}):
    """
    Build a dataset for new registrations using a schema and data content.

    Args:
        _schema (str, optional): Name of the schema/entity.
        data_content (dict, optional): Data to populate the schema.

    Returns:
        dict: Dataset built from the schema and data content.
    """
    dataset = {}
    import ipdb; ipdb.set_trace()
    for k, v in data_content.items():
        if k in schemas[_schema]().load_fields.keys():
            dataset.update({k: v})
            if _schema == "sales":
                dataset["cart_id"] = data_content.get("id")
    schema_true, msg = schema_validator(_schema, dataset)
    if schema_true:         
        return dataset
    return dataset