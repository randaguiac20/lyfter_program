from marshmallow import (Schema, fields,
                         validate, ValidationError)



class StrOrList(fields.List):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            value = [value]
        elif not isinstance(value, list):
            raise ValidationError("Field should be a string or a list of strings.")
        return super()._deserialize(value, attr, data, **kwargs)

class RoleSchema(Schema):
    id = fields.Str(required=False)
    role_name = fields.Str(required=True)
    description = fields.Str(required=True)

class ProductRegistrationSchema(Schema):
    id = fields.Str(required=False)
    product_id = fields.Str(required=False)
    inventory_id = fields.Str(required=False)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    size = fields.Str(required=True)
    breed_size = fields.Str(required=True)
    brand = fields.Str(required=True)
    description = fields.Str(required=True)
    ingress_date = fields.DateTime(required=True, format="%d_%m_%Y")
    expiration_date = fields.DateTime(required=True, format="%d_%m_%Y")
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["registered", 
                             "unregistered"]))

class UserRegistrationSchema(Schema):
    id = fields.UUID(required=False)
    user_id = fields.Str(required=False)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)
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
    id = fields.UUID(required=False)
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
    id = fields.Str(required=False)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    size = fields.Str(required=True)
    breed_size = fields.Str(required=True)
    brand = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["active", 
                             "disable"]))

class SaleSchema(Schema):
    id = fields.Str(required=False)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["in_progress", 
                             "to_be_done", 
                             "completed"]))

class InventorySchema(Schema):
    id = fields.Str(required=False)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    size = fields.Str(required=True)
    breed_size = fields.Str(required=True)
    brand = fields.Str(required=True)
    quantity = fields.Int(required=False, load_default=0)
    description = fields.Str(required=True)
    ingress_date = fields.DateTime(required=True, format="%d_%m_%Y")
    expiration_date = fields.DateTime(required=True, format="%d_%m_%Y")
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["active", 
                             "disable"]))


# Schema mapper
schemas = {
    "role": RoleSchema,
    "user_registration": UserRegistrationSchema,
    "product_registration": ProductRegistrationSchema,
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
    
def schema_builder_for_new_registrations(_schema=None, data_content={}):
    dataset = {}
    for k,v in data_content.items():
        if k in schemas[_schema]().load_fields.keys():
            dataset.update({k:v})
    schema_true, msg = schema_validator(_schema, data_content)
    if schema_true:         
        return dataset
    return dataset
    