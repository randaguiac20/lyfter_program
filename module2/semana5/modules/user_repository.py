import json
from flask import (Flask, request, jsonify)
from modules.config import user_fields
from datetime import date
from modules.repository import Repository



class UserRepository(Repository):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.manager = db_manager
    
    def _format_user(self, user_record):
        return {
            "id": user_record[0],
            "first_name": user_record[1],
            "last_name": user_record[2],
            "email": user_record[3],
            "username": user_record[4],
            "account_status": user_record[6]
        }

    def get(self, option=None):
        try:
            if option.split("=")[0] in user_fields:
                key = option.split("=")[0]
            else:
                key = option.split("=")[0]
                return jsonify({"Error":f"Option: '{key}' is NOT valid."}), 404
            value = option.split("=")[1]
        except Exception:
            jsonify({"Error":"Bad request wrong field or wrong format."}), 400
        users = []
        if option is None:
            query = "SELECT * FROM lyfter_car_rental.users;"
            results = self.manager.execute_query(query)
            for result in results or []:
                users.append(self._format_user(result))
        else:
            query = "SELECT * FROM lyfter_car_rental.users WHERE {key} = %s;"
            results = self.manager.execute_query(query, (value,))
            if results:
                users.append(self._format_user(results[0]))
        return jsonify(users)

    def post(self):
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get("email").lower()
        username = request.json.get("username").lower()
        password = request.json.get("password")
        birthday = request.json.get("birthday").lower()
        account_status = request.json.get("account_status").lower()
        # Placeholder for create logic using self.manager
        query = f"SELECT * FROM lyfter_car_rental.users WHERE email = %s;"
        _result = self.manager.execute_query(query, (email,))
        if _result:
            return jsonify(self._format_user(_result[0]))
        query = """INSERT INTO lyfter_car_rental.users 
                   (first_name, last_name, email, username, password, birthday, account_status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        self.manager.execute_query(query, (first_name, last_name, email, username, password,
                                           birthday, account_status,))
        request.json.pop("password")
        result = request.json
        return jsonify(result)
    
    def put(self):
        username = request.json.get("username").lower()
        account_status = request.json.get("account_status").lower()
        user = self.get(username)
        query = "UPDATE lyfter_car_rental.users SET account_status = %s WHERE id = %s;"
        try:
            user_id = user.json[0].get("id")
        except IndexError:
            return jsonify({"info":"No user with this username in our records."})
        self.manager.execute_query(query, (account_status, user_id,))
        user = self.get(username)
        return jsonify(user.json)

    def delete(self):
        pass

