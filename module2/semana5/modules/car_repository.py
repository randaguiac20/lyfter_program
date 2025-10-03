import json
from flask import (Flask, request, jsonify)
from modules.config import car_fields
from datetime import date
from repository import Repository


class CarRepository(Repository):
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
