"""repository.py

Base repository abstract class defining the interface for all API repositories.
Combines Flask's MethodView with abstract base class pattern for consistent API structure.
"""

from abc import ABC, abstractmethod
from flask.views import MethodView


class Repository(ABC, MethodView):
    """
    Abstract base repository class.
    
    Defines the standard CRUD interface that all repository classes must implement.
    Inherits from both ABC (Abstract Base Class) and Flask's MethodView for
    handling HTTP methods.
    
    All concrete repository classes must implement get, post, put, and delete methods.
    """
    
    @abstractmethod
    def get(self):
        """
        Handle GET requests - retrieve records.
        
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def post(self):
        """
        Handle POST requests - create new records.
        
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def put(self):
        """
        Handle PUT requests - update existing records.
        
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Handle DELETE requests - remove records.
        
        Must be implemented by subclasses.
        """
        pass
