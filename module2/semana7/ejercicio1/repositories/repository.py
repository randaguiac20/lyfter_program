from abc import ABC, abstractmethod
from flask.views import MethodView


class Repository(ABC, MethodView):
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
