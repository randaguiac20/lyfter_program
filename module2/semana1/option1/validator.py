import os
import csv
import inspect
from functools import wraps
from marshmallow import (Schema, fields,
                         validate)

class TaskSchema(Schema):
    task_id = fields.Str(required=False)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True,
                        validate=validate.OneOf(
                            ["in_progress", 
                             "to_be_done", 
                             "completed"]))


def check_file_not_found(create_if_missing=False,
                         file_type="txt", headers=None):
    """
    I DID NOT DO THIS BY MY OWN
    I HAD TO LOOK FOR EXAMPLES TO BUILD THIS DECORATOR
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except FileNotFoundError as e:
                if create_if_missing:
                    # Use inspect to resolve all arguments including defaults
                    sig = inspect.signature(func)
                    bound = sig.bind(self, *args, **kwargs)
                    bound.apply_defaults()
                    data_filename = bound.arguments.get('finance_filename')
                    if file_type == "csv" and data_filename:
                        with open(data_filename, 'w', encoding='utf-8', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(headers)
                            
                            print(f"File was created!!")
                            return func(self, *args, **kwargs)
                print(f"Error: {e}. Please check the file path.")
                return None
        return wrapper
    return decorator
