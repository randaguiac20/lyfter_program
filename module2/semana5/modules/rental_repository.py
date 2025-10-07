import json
from flask import (Flask, request, jsonify)
from modules.config import rentacar_fields
from datetime import date
from modules.repository import Repository


class RentCarUsers(Repository):
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