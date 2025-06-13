"""
validator.py

Provides validation utilities and decorators for API request data.
"""

import json
import inspect
from functools import wraps
from flask import request, jsonify
from pathlib import Path
from configurations.config import endpoint_fields_mapper

def content_mapper(file_data, request_data, option):
    """
    Check if a record with the same key fields exists in the file data.

    Args:
        file_data (list): List of existing records.
        request_data (dict): Data to check.
        option (str): The entity type.

    Returns:
        bool: True if a matching record exists, False otherwise.
    """
    efm = endpoint_fields_mapper.get(option)
    result = any(d.get(efm[0]) == request_data.get(efm[0]) and
                 d.get(efm[1]) == request_data.get(efm[1]) and
                 d.get(efm[2]) == request_data.get(efm[2])
                 for d in file_data)
    return result

def dir_or_file_exists(filepath, option="Directory"):
    """
    Check if a directory or file exists.

    Args:
        filepath (str): Path to check.
        option (str): Type of path ("Directory" or "File").

    Returns:
        bool: True if exists, False otherwise.
    """
    dir_path = Path(filepath)
    if dir_path.exists():
        print(f"{option} exists")
        return True
    return False

def reject_fields(*forbidden_fields):
    """
    Decorator to reject requests containing forbidden fields.

    Args:
        *forbidden_fields: Fields not allowed in the request.

    Returns:
        function: Decorated function that rejects forbidden fields.
    """
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