from abc import ABC, abstractmethod
from flask.views import MethodView
import json
from flask import (Flask, request, jsonify)
from modules.config import user_fields, car_fields, rentacar_fields
from datetime import date



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

class CarRepository(MethodView):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.manager = db_manager

    def _format_car(self, car_record):
        manufactured_year = car_record[3]
        # Convert date object to string format YYYY-MM-DD
        if isinstance(manufactured_year, date):
            manufactured_year = manufactured_year.strftime('%Y-%m-%d')
        return {
            "id": car_record[0],
            "brand": car_record[1],
            "model": car_record[2],
            "manufactured_year": manufactured_year,
            "state": car_record[4],
            "status": car_record[5]
        }

    def get(self, option=None):
        try:
            if option.split("=")[0] in car_fields:
                key = option.split("=")[0]
            else:
                key = option.split("=")[0]
                return jsonify({"Error":f"Option: '{key}' is NOT valid."}), 404
            value = option.split("=")[1]
        except Exception:
            jsonify({"Error":"Bad request wrong field or wrong format."}), 400
        cars = []
        if option is None:
            query = "SELECT * FROM lyfter_car_rental.cars;"
            results = self.manager.execute_query(query)
            for result in results or []:
                cars.append(self._format_car(result))
        else:
            query = f"SELECT * FROM lyfter_car_rental.cars WHERE {key} = %s;"
            results = self.manager.execute_query(query, (value,))
            if results:
                cars.append(self._format_car(results[0]))
        return jsonify(cars)
    
    def post(self):
        brand = request.json.get("brand").lower()
        model = request.json.get("model").lower()
        manufactured_year = request.json.get("manufactured_year")
        state = request.json.get("state").lower()
        status = request.json.get("status").lower()
        # Placeholder for create logic using self.manager
        query = f"SELECT * FROM lyfter_car_rental.cars WHERE model = %s;"
        _result = self.manager.execute_query(query, (model,))
        if _result:
            return jsonify(self._format_car(_result[0]))
        query = """INSERT INTO lyfter_car_rental.cars 
                   (brand, model, manufactured_year, state, status) 
                   VALUES (%s, %s, %s, %s, %s)"""
        self.manager.execute_query(query, (brand, model, manufactured_year, state, status))
        result = request.json
        return jsonify(result)
    
    def put(self):
        model = request.json.get("model").lower()
        status = request.json.get("status").lower()
        car = self.get(model)
        query = "UPDATE lyfter_car_rental.cars SET status = %s WHERE id = %s;"
        try:
            car_id = car.json[0].get("id")
        except IndexError:
            return jsonify({"info":"Car model NOT found in our records."})
        self.manager.execute_query(query, (status, car_id,))
        car = self.get(model)
        return jsonify(car.json)
    
    def delete(self):
        pass

class RentCarUsers(MethodView):
    def __init__(self, db_manager, *args, **kwargs):
        # Ensure MethodView init runs and accept extra args if Flask passes any
        super().__init__(*args, **kwargs)
        self.manager = db_manager

    def _format_rentcar(self, rentcar_record):
        rent_date = rentcar_record[4]
        # Convert date object to string format YYYY-MM-DD
        if isinstance(rent_date, date):
            rent_date = rent_date.strftime('%Y-%m-%d')
        return {
            "id": rentcar_record[0],
            "user_id": rentcar_record[1],
            "car_id": rentcar_record[2],
            "status": rentcar_record[3],
            "rent_date": rent_date
        }
    
    def get_user(self, username):
        query = "SELECT * FROM lyfter_car_rental.users WHERE username = %s;"
        results = self.manager.execute_query(query, (username,))
        if results:
            user = results[0][0]
            return user
        return None

    def get_car(self, model):
        query = "SELECT * FROM lyfter_car_rental.cars WHERE model = %s;"
        results = self.manager.execute_query(query, (model,))
        if results:
            car = results[0][0]
            return car
        return None

    def get(self, option=None):
        try:
            if option.split("=")[0] in rentacar_fields:
                key = option.split("=")[0]
            else:
                key = option.split("=")[0]
                return jsonify({"Error":f"Option: '{key}' is NOT valid."}), 404
            value = option.split("=")[1]
        except Exception:
            jsonify({"Error":"Bad request wrong field or wrong format."}), 400
        rentcars = []
        if option is None:
            query = "SELECT * FROM lyfter_car_rental.rentcar_users;"
            results = self.manager.execute_query(query)
            for result in results or []:
                rentcars.append(self._format_rentcar(result))
        else:
            query = f"SELECT * FROM lyfter_car_rental.rentcar_users WHERE {key} = %s;"
            results = self.manager.execute_query(query, (value,))
            if results:
                rentcars.append(self._format_rentcar(results[0]))
        return jsonify(rentcars)
    
    def post(self):
        username = request.json.get("username").lower()
        model = request.json.get("model").lower()
        status = request.json.get("status").lower()
        rent_date = request.json.get("rent_date")
        return_date = request.json.get("return_date")
        user_id = self.get_user(username)
        if user_id is None:
            return jsonify({"info":"No user with this username in our records."})
        car_id = self.get_car(model)
        if car_id is None:
            return jsonify({"info":"This brand is not available in our records."})
        # Placeholder for create logic using self.manager
        query = """INSERT INTO lyfter_car_rental.rentcar_users 
                   (user_id, car_id, status, rent_date, return_date) 
                   VALUES (%s, %s, %s, %s, %s)"""
        self.manager.execute_query(query, (user_id, car_id, status, rent_date, return_date,))
        result = request.json
        return jsonify(result)
    
    def put(self):
        id = request.json.get("id")
        status = request.json.get("status").lower()
        return_date = request.json.get("return_date")
        rentcar = self.get(id)
        query = "UPDATE lyfter_car_rental.rentcar_users SET status = %s, return_date = %s WHERE id = %s;"
        try:
            rent_id = rentcar.json[0].get("id")
        except IndexError:
            return jsonify({"info":"Car rent NOT found in our records."})
        self.manager.execute_query(query, (status, return_date, rent_id,))
        rentcar = self.get(id)
        return jsonify(rentcar.json)
    
    def delete(self):
        pass