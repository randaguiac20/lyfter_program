import json
import inspect
from functools import wraps
from flask import request, jsonify
from pathlib import Path
from configurations.config import endpoint_fields_mapper


def duplicate_content_checker(file_data, request_data, option):
    efm = endpoint_fields_mapper.get(option)
    result = any(d.get(efm[0]) == request_data.get(efm[0]) or
                         d.get(efm[1]) == request_data.get(efm[1]) and
                         d.get(efm[2]) == request_data.get(efm[2])
                         for d in file_data)
    return result


def dir_or_file_exists(filepath, option="Directory"):
    dir_path = Path(filepath)
    # Check if directory exists
    if dir_path.exists():
        print(f"{option} exists")
        return True
    return False

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
