"""models.py

SQLAlchemy ORM models for the Fruit Products API.

Defines all database models including:
    - UserRegistration: Authentication credentials and roles.
    - User: User profile information.
    - UserContact: User contact details.
    - Address: User addresses.
    - Product: Product inventory.
    - ShoppingCart: Shopping cart with status tracking.
    - Receipt: Purchase receipts.
    - ShoppingCartProduct: Junction table for cart-product relationships.

Also includes the CartStatus enum and input validation functions.
"""

from sqlalchemy import (Enum, Column, Integer, String, DateTime, 
                        Boolean, func, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship
from modules.config import Base
import enum



def validate_buy_fruits(record_input):
    """
    Validate input data for the buy-fruits endpoint.
    
    Args:
        record_input (dict): Dictionary containing product purchase details.
            Required keys: 'name' (str), 'size' (str), 'quantity' (int).
            
    Returns:
        tuple: (bool, str) - (True, "Valid data") if valid,
               (False, error_message) if invalid.
    """""
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
    """
    Enumeration for shopping cart status values.
    
    Values:
        ACTIVE: Cart is active and can be modified.
        PENDING: Cart is pending checkout.
        COMPLETED: Purchase has been completed.
        CANCELLED: Cart has been cancelled.
    """
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class UserRegistration(Base):
    """
    User registration model for authentication credentials.
    
    Stores email, hashed password, and role for user authentication.
    Has a one-to-one relationship with User model.
    
    Attributes:
        id (int): Primary key.
        email (str): Unique email address.
        password (str): Hashed password.
        role (str): User role ('administrator' or 'client').
        created_at (datetime): Record creation timestamp.
        updated_at (datetime): Record update timestamp.
        user: Related User object.
    """
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
    """
    User profile model containing personal information.
    
    Stores user details and links to registration, address, contacts, and carts.
    
    Attributes:
        id (int): Primary key.
        registration_id (int): Foreign key to UserRegistration.
        first_name (str): User's first name.
        last_name (str): User's last name.
        telephone (str): Unique phone number (8 digits).
        address_id (int): Foreign key to Address.
        created_at (datetime): Record creation timestamp.
        updated_at (datetime): Record update timestamp.
        contacts: Related UserContact objects.
        address: Related Address object.
        carts: Related ShoppingCart objects.
        register_user: Related UserRegistration object.
    """
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
    """
    User contact model for storing additional contact information.
    
    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to User.
        created_at (datetime): Record creation timestamp.
        updated_at (datetime): Record update timestamp.
        user: Related User object.
    """
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
    """
    Address model for storing user addresses.
    
    Stores street address, city, state, postal code, and country.
    Multiple users can share the same address.
    
    Attributes:
        id (int): Primary key.
        street (str): Street address.
        city (str): City name.
        state (str): State/province name.
        postal_code (str): Postal/ZIP code.
        country (str): Country name (default: USA).
        created_at (datetime): Record creation timestamp.
        updated_at (datetime): Record update timestamp.
        users: List of related User objects.
    """
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
    """
    Product model for the fruit inventory.
    
    Stores product information including name, description, price, size, and quantity.
    Unique constraint on combination of name, price, and size.
    
    Attributes:
        id (int): Primary key.
        name (str): Product name.
        description (str): Product description.
        price (int): Price in cents/smallest currency unit.
        size (str): Product size ('large', 'medium', 'small').
        quantity (int): Available inventory quantity.
        created_at (datetime): Record creation timestamp.
        updated_at (datetime): Record update timestamp.
        cart_products: Related ShoppingCartProduct objects.
    """
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
    """
    Shopping cart model for tracking user purchases.
    
    Represents a shopping session with status tracking.
    Links to user, receipt, and cart products.
    
    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to User.
        status (CartStatus): Cart status enum.
        purchase_date (datetime): Date of purchase.
        created_at (datetime): Record creation timestamp.
        updated_at (datetime): Record update timestamp.
        user: Related User object.
        receipt: Related Receipt object.
        cart_products: List of ShoppingCartProduct objects.
    """
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
    """
    Receipt model for purchase records.
    
    Stores payment information and total amount for completed purchases.
    
    Attributes:
        id (int): Primary key.
        cart_id (int): Foreign key to ShoppingCart.
        description (str): Receipt description.
        payment_method (str): Payment method used.
        total_amount (int): Total purchase amount.
        created_at (datetime): Record creation timestamp.
        updated_at (datetime): Record update timestamp.
        cart: Related ShoppingCart object.
    """
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
    """
    Junction model linking shopping carts to products.
    
    Stores the quantity and checkout status for each product in a cart.
    
    Attributes:
        id (int): Primary key.
        cart_id (int): Foreign key to ShoppingCart.
        product_id (int): Foreign key to Product.
        quantity (int): Quantity of the product.
        checkout (bool): Whether item has been checked out.
        created_at (datetime): Record creation timestamp.
        updated_at (datetime): Record update timestamp.
        product: Related Product object.
        cart: Related ShoppingCart object.
    """
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
