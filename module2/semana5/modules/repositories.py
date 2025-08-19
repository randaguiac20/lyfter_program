from abc import ABC, abstractmethod
from flask.views import MethodView
from modules.config import user_repo_queries


class Repository(ABC):
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def update(self):
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
            for row in results or []:
                users.append(self._format_user(row))
        else:
            query = f"SELECT * FROM lyfter_car_rental.users WHERE id = {id};"
            results = self.manager.execute_query(query, id)
            if results:
                users.append(self._format_user(results[0]))
        return users

    def post(self):
        # Placeholder for create logic using self.manager
        return {"message": "Not implemented"}, 501
    
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