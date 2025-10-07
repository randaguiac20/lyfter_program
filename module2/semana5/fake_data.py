import factory
from factory import Faker, SubFactory
from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Database setup
DATABASE_URL = "postgresql://randall_aguilar:lyfter_password@localhost:5450/lyfter"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'lyfter_car_rental'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    account_status = Column(String(50), nullable=False)
    birthday = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(),
                       onupdate=func.current_timestamp())

    # Relationship
    rentals = relationship("RentCarUser", back_populates="user")

    __table_args__ = (
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'",
            name='email_format_check'
        ),
        {'schema': 'lyfter_car_rental'}
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Car(Base):
    __tablename__ = 'cars'
    __table_args__ = {'schema': 'lyfter_car_rental'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    manufactured_year = Column(Date, nullable=False)
    state = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp())
    
    # Relationship
    rentals = relationship("RentCarUser", back_populates="car")
    
    def __repr__(self):
        return f"<Car(id={self.id}, brand='{self.brand}', model='{self.model}')>"


class RentCarUser(Base):
    __tablename__ = 'rentcar_users'
    __table_args__ = {'schema': 'lyfter_car_rental'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('lyfter_car_rental.users.id', ondelete='CASCADE'), nullable=False)
    car_id = Column(Integer, ForeignKey('lyfter_car_rental.cars.id', ondelete='CASCADE'), nullable=False)
    status = Column(String(25), nullable=False)
    rent_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp())
    
    # Relationships
    user = relationship("User", back_populates="rentals")
    car = relationship("Car", back_populates="rentals")
    
    def __repr__(self):
        return f"<RentCarUser(id={self.id}, user_id={self.user_id}, car_id={self.car_id}, status='{self.status}')>"


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'commit'

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    username = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}"
    )
    password = Faker('password', length=12)
    account_status = Faker('random_element', elements=('active', 'inactive', 'suspended'))
    birthday = Faker('date_of_birth', minimum_age=18, maximum_age=80)


class CarFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Car
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'commit'

    brand = Faker('random_element', elements=(
        'Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes-Benz',
        'Audi', 'Volkswagen', 'Nissan', 'Hyundai', 'Kia', 'Mazda',
        'Subaru', 'Tesla', 'Lexus', 'Jeep', 'Ram', 'GMC'
    ))
    
    model = factory.LazyAttribute(lambda obj: {
        'Toyota': random.choice(['Camry', 'Corolla', 'RAV4', 'Highlander', 'Tacoma']),
        'Honda': random.choice(['Civic', 'Accord', 'CR-V', 'Pilot', 'Odyssey']),
        'Ford': random.choice(['F-150', 'Mustang', 'Explorer', 'Escape', 'Bronco']),
        'Chevrolet': random.choice(['Silverado', 'Malibu', 'Equinox', 'Tahoe', 'Camaro']),
        'BMW': random.choice(['3 Series', '5 Series', 'X3', 'X5', 'M4']),
        'Mercedes-Benz': random.choice(['C-Class', 'E-Class', 'GLC', 'GLE', 'S-Class']),
        'Audi': random.choice(['A4', 'A6', 'Q5', 'Q7', 'e-tron']),
        'Volkswagen': random.choice(['Jetta', 'Passat', 'Tiguan', 'Atlas', 'Golf']),
        'Nissan': random.choice(['Altima', 'Sentra', 'Rogue', 'Pathfinder', 'Maxima']),
        'Hyundai': random.choice(['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona']),
        'Kia': random.choice(['Forte', 'Optima', 'Sportage', 'Sorento', 'Telluride']),
        'Mazda': random.choice(['Mazda3', 'Mazda6', 'CX-5', 'CX-9', 'MX-5']),
        'Subaru': random.choice(['Impreza', 'Legacy', 'Outback', 'Forester', 'Crosstrek']),
        'Tesla': random.choice(['Model 3', 'Model S', 'Model X', 'Model Y']),
        'Lexus': random.choice(['ES', 'IS', 'RX', 'NX', 'GX']),
        'Jeep': random.choice(['Wrangler', 'Grand Cherokee', 'Cherokee', 'Compass', 'Gladiator']),
        'Ram': random.choice(['1500', '2500', '3500', 'ProMaster']),
        'GMC': random.choice(['Sierra', 'Terrain', 'Acadia', 'Yukon', 'Canyon'])
    }.get(obj.brand, 'Standard'))
    
    manufactured_year = Faker('date_between', start_date='-10y', end_date='-1y')
    
    state = Faker('random_element', elements=(
        'excellent', 'good', 'fair', 'needs_maintenance', 'in_repair'
    ))
    
    status = Faker('random_element', elements=(
        'available', 'rented', 'maintenance', 'reserved', 'retired'
    ))


class RentCarUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RentCarUser
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'commit'

    # Use SubFactory to create or reference existing users/cars
    user = SubFactory(UserFactory)
    car = SubFactory(CarFactory)
    
    status = Faker('random_element', elements=(
        'active', 'completed', 'cancelled', 'pending', 'overdue'
    ))
    
    rent_date = Faker('date_between', start_date='-1y', end_date='today')
    
    return_date = factory.LazyAttribute(
        lambda obj: Faker('date_between', 
                         start_date=obj.rent_date, 
                         end_date=obj.rent_date + timedelta(days=random.randint(1, 60))
                        ).evaluate(None, None, {'locale': None}) 
        if random.random() > 0.3 else None
    )


def generate_data():
    num_users = 200
    num_cars = 100
    num_rentals = 150
    session = Session()
    try:
        UserFactory._meta.sqlalchemy_session = session
        CarFactory._meta.sqlalchemy_session = session
        RentCarUserFactory._meta.sqlalchemy_session = session
        print("Start populating tables..\n")
        print("Populating user table...")
        users = UserFactory.create_batch(num_users)
        print("Finished populating user table.\n")
        print("Populating car table...")
        cars = CarFactory.create_batch(num_cars)
        print("Finished populating car table.\n")
        print("Populating rentals table...")
        user_ids = [user.id for user in session.query(User).all()]
        car_ids = [car.id for car in session.query(Car).all()]
        rentals = []
        for record in range(num_rentals):
            rental = RentCarUserFactory.build()
            rental.user_id = random.choice(user_ids)
            rental.car_id = random.choice(car_ids)
            session.add(rental)
            rentals.append(rental)
            if (record + 1) % 50 == 0:
                session.commit()
        session.commit()
        print("Finished populating rental table.\n")
    except Exception as e:
        session.rollback()
        print(f"\nError occurred: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    data_generator = generate_data()
