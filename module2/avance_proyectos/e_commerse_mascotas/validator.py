import os
import json
import inspect
from functools import wraps
from flask import request, jsonify
from marshmallow import (Schema, fields,
                         validate)


class UserSchema(Schema):
    user_id = fields.UUID(required=False)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)
    description = fields.Str(required=False)
    last_modified = fields.DateTime(required=True, format="%d_%m_%Y-%H:%M")
    status = fields.Str(required=False,
                        validate=validate.OneOf(
                            ["registered", 
                             "unregistered"]))

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
    
class RoleSchema(Schema):
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

def check_file_not_found(create_if_missing=False,
                         json_filename=None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except FileNotFoundError as e:
                if create_if_missing:
                    # Use inspect to resolve all arguments including defaults
                    sig = inspect.signature(args.get("filename"))
                    bound = sig.bind(self, *args, **kwargs)
                    bound.apply_defaults()
                    data_filename = bound.arguments.get(json_filename)
                    if data_filename:
                        with open(data_filename, 'w', encoding='utf-8', newline='') as file:
                            json.dump({}, file, indent=4)
                            
                            print(f"File was created!!")
                            return func(self, *args, **kwargs)
                print(f"Error: {e}. Please check the file path.")
                return None
        return wrapper
    return decorator

def reject_fields(*forbidden_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json() or {}
            for field in forbidden_fields:
                if field in data:
                    return jsonify({"error": f"Field '{field}' is not allowed"}), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator
