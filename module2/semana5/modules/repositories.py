from abc import ABC, abstractmethod

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
    
    
class UserRepository:
    def create(self):
        pass
    
    def update(self):
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