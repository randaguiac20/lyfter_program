from sqlalchemy import (Column, Integer, String, DateTime, 
                        func, ForeignKey)
from sqlalchemy.orm import relationship
from modules.config import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    address = relationship("Address", back_populates="user")
    car = relationship("Car", back_populates="user")

    def __repr__(self):
        return f"User id={self.id}, name='{self.first_name} {self.last_name}', email='{self.email}'"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100), default="USA", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="address")

    def __repr__(self):
        try:
            user_name = f"{self.user.first_name} {self.user.last_name}"
        except:
            user_name = "No user found"
        return f"Address id={self.id}, user name={user_name} city='{self.city}', state='{self.state}', country='{self.country}'"


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    brand = Column(String(50))
    model = Column(String(50))
    manufactured_year = Column(String(50))
    status = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    user = relationship("User", back_populates="car")

    def __repr__(self):
        try:
            user_name = f"{self.user.first_name} {self.user.last_name}"
        except:
            user_name = "No owner"
        return f"Cars id={self.id}, owner='{user_name}', brand='{self.brand}', model='{self.model}', manufactured year='{self.manufactured_year}'"


_models = {
    "user": User,
    "address": Address,
    "car": Car
}