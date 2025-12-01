# main.py (or wherever you bootstrap)
from modules.db_manager import DBManager


if __name__ == '__main__':
    db = DBManager()
    # Insert users
    user1 = db.insert("User", first_name="John", last_name="Doe", email="john.doe@example.com")
    user2 = db.insert("User", first_name="Jane", last_name="Smith", email="jane.smith@example.com")
    user3 = db.insert("User", first_name="Michael", last_name="Johnson", email="michael.johnson@example.com")

    # Insert addresses
    db.insert("Address", street="123 Main Street", city="New York", state="NY", postal_code="10001", country="USA", user_id=user1.id)
    db.insert("Address", street="456 Oak Avenue", city="Los Angeles", state="CA", postal_code="90001", country="USA", user_id=user2.id)
    db.insert("Address", street="789 Pine Road", city="Chicago", state="IL", postal_code="60601", country="USA", user_id=user3.id)

    # Insert cars
    db.insert("Car", brand="Toyota", model="Camry", manufactured_year="2022", status="active", user_id=user1.id)
    db.insert("Car", brand="Honda", model="Civic", manufactured_year="2021", status="active", user_id=user2.id)
    db.insert("Car", brand="Ford", model="F-150", manufactured_year="2023", status="maintenance", user_id=user3.id)

    users = db.get("user")
    addresses = db.get("address")
    cars = db.get("car")
    print("============================================================================")
    for user in users:
        print(user)
    print("============================================================================")
    for address in addresses:
        print(address)
    print("============================================================================")
    for car in cars:
        print(car)
    print("============================================================================")
    db.close()