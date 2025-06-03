from marshmallow import (Schema, fields,
                         validate, ValidationError)



class RoleSchema(Schema):
    role_id = fields.Str(required=False)
    role_name = fields.Str(required=True)
    description = fields.Str(required=True)

class UserRegistrationSchema(Schema):
    user_id = fields.UUID(required=False)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)
    description = fields.Str(required=False)
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    role = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["administrator", 
                             "client"]))
    status = fields.Str(required=False,
                        validate=validate.OneOf(
                            ["registered", 
                             "unregistered"]))

class UserSchema(Schema):
    user_id = fields.UUID(required=False)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)
    description = fields.Str(required=False)
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=False,
                        validate=validate.OneOf(
                            ["active", 
                             "disable"]))

class ProductSchema(Schema):
    task_id = fields.Str(required=False)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["in_progress", 
                             "to_be_done", 
                             "completed"]))

class SaleSchema(Schema):
    task_id = fields.Str(required=False)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["in_progress", 
                             "to_be_done", 
                             "completed"]))

class InventorySchema(Schema):
    task_id = fields.Str(required=False)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["in_progress", 
                             "to_be_done", 
                             "completed"]))

schemas = {
    "role": RoleSchema,
    "user_registration": UserRegistrationSchema,
    "user": UserSchema,
    "product": ProductSchema,
    "sales": SaleSchema,
    "inventory": InventorySchema
}

def schema_validator(schema, request_data):
    _schema = schemas.get(schema)()
    try:
        _schema.load(request_data)
        msg = "good"
        return True, msg
    except ValidationError as err:
        msg = f"error: Validation failed, messages: {err.messages}"
        return False, msg