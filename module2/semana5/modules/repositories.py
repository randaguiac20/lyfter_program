from abc import ABC, abstractmethod
from flask.views import MethodView
from flask import (Flask, request, jsonify)
from modules.config import user_repo_queries



class Repository(ABC):
    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def delete(self):
        pass
    
    
class UserRepository(MethodView):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.manager = db_manager
        self.user_queries = user_repo_queries
    
    def _format_user(self, user_record):
        return {
            "id": user_record[0],
            "first_name": user_record[1],
            "last_name": user_record[2],
            "email": user_record[3],
            "username": user_record[4],
        }

    def get(self, id=None):
        users = []
        if id is None:
            query = "SELECT * FROM lyfter_car_rental.users;"
            results = self.manager.execute_query(query)
            for result in results or []:
                users.append(self._format_user(result))
        else:
            query = f"SELECT * FROM lyfter_car_rental.users WHERE id = %s;"
            results = self.manager.execute_query(query, (id,))
            if results:
                users.append(self._format_user(results[0]))
        return jsonify(users)

    def post(self):
        # first_name = request.json.get("first_name")
        # last_name = request.json.get("last_name")
        email = request.json.get("email")
        # username = request.json.get("username")
        # password = request.json.get("password")
        # birthday = request.json.get("birthday")
        account_status = request.json.get("account_status")
        # Placeholder for create logic using self.manager
        query = f"SELECT * FROM lyfter_car_rental.users WHERE email = %s;"
        _result = self.manager.execute_query(query, (email,))
        if _result:
            return jsonify(self._format_user(_result[0]))
        query = """INSERT INTO lyfter_car_rental.users 
                   (first_name, last_name, email, username, password, birthday, account_status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        self.manager.execute_query(query, (request.json))
        request.json.pop("password")
        result = request.json
        return jsonify(result)
    
    def put(self):
        pass
    
    def delete(self):
        pass

class CarRepository:
    def create(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass

class RentCarUsers:
    def create(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass