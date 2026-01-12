from sqlalchemy import (Enum, Column, Integer, String, DateTime, 
                        Boolean, func, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship
from modules.config import Base
import enum



def validate_buy_fruits(record_input):
    """Validate buy-fruits input data"""
    if not isinstance(record_input, dict):
        return False, "Invalid format."
    reguired_fields = {"name", "size", "quantity"}
    default_sizes = ["large", "medium", "small"]
    if set(record_input.keys()) != reguired_fields:
        return False, f"Must provide the correct fields, correct fields are {reguired_fields}"
    
    # Validate types
    if not isinstance(record_input.get("name"), str):
        return False, "Invalid value type, 'name' must be a string."
    
    if not isinstance(record_input.get("size"), str) or not record_input["size"] in default_sizes:
        return False, "Invalid value type, 'price' must be a positive integer"
    
    if not isinstance(record_input.get("quantity"), int) or record_input["quantity"] <= 0:
        return False, "Invalid value type, 'quantity' must be a positive integer"
    return True, "Valid data"
    

class CartStatus(enum.Enum):
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class UserRegistration(Base):
    __tablename__ = "user_registrations"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String(255))
    role = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # UserContact = class name, back_populates = field name i.e user on other table/class
    user = relationship("User", back_populates="register_user", uselist=False,
                        cascade="all, delete-orphan")

    def __repr__(self):
        return f"Register User id={self.id}, email='{self.email}'"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', 'telephone', name='unique_user_identity'),
    )

    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey("user_registrations.id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    telephone = Column(String(8), unique=True)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # UserContact = class name, back_populates = field name i.e user on other table/class
    contacts = relationship("UserContact", back_populates="user",
                            cascade="all, delete-orphan")
    address = relationship("Address", back_populates="users", uselist=False)
    carts = relationship("ShoppingCart", back_populates="user",
                         cascade="all, delete-orphan")
    register_user = relationship("UserRegistration", back_populates="user", uselist=False)

    def __repr__(self):
        fields = []
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            fields.append(f"{column.name}={value!r}")
        return f"User: {', '.join(fields)}"


class UserContact(Base):
    __tablename__ = "user_contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="contacts")
    

    def __repr__(self):
        user_name = (
            f"{self.user.first_name} {self.user.last_name}"
            if self.user else "No user"
        )
        return f"User contact id={self.id}, user_name='{user_name}', email='{self.user.email}'"


class Address(Base):
    __tablename__ = "addresses"
    __table_args__ = (
        UniqueConstraint('street', 'city', 'postal_code', name='unique_address'),
    )

    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100), default="USA", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    users = relationship("User", back_populates="address")

    def __repr__(self):
        _users = (
            f"{self.users}"
        )
        return f"Address id={self.id}, users={_users} city='{self.city}', state='{self.state}', country='{self.country}'"


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint('name', 'price', 'size', name='unique_product_identity'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(85))
    description = Column(String(100))
    price = Column(Integer)
    size = Column(String)
    quantity = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cart_products = relationship("ShoppingCartProduct", back_populates="product")

    def __repr__(self):
        return f"Product id={self.id}, Product name={self.name}, Price={self.price}, Size={self.size}"


class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(CartStatus), default=CartStatus.ACTIVE, nullable=False)
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="carts")
    receipt = relationship("Receipt", back_populates="cart", uselist=False)
    cart_products = relationship("ShoppingCartProduct", back_populates="cart")

    def __repr__(self):
        user_name = (
            f"{self.user.first_name} {self.user.last_name}"
            if self.user else "No user"
        )
        return f"Cart id={self.id}, user_name='{user_name}'"


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"), nullable=False)
    description = Column(String(100))
    payment_method = Column(String(50))
    total_amount = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cart = relationship("ShoppingCart", back_populates="receipt", uselist=False)

    def __repr__(self):
        return f"Receipt id={self.id}, Payment method={self.payment_method}"


class ShoppingCartProduct(Base):
    __tablename__ = "cart_products"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("shopping_carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer)
    checkout = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    product = relationship("Product", back_populates="cart_products")
    cart = relationship("ShoppingCart", back_populates="cart_products")

    def __repr__(self):
        return f"Shopping Cart Product id={self.id}"


_models = {
    "register_user": UserRegistration,
    "user": User,
    "user_contact": UserContact,
    "address": Address,
    "product": Product,
    "shopping_cart": ShoppingCart,
    "receipt": Receipt,
    "shopping_cart_product": ShoppingCartProduct
}
