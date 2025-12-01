# main.py (or wherever you bootstrap)
from modules.db_manager import DBManager


if __name__ == '__main__':
    db = DBManager()
    # Sample data for 20 users
    users_data = [
        {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com"},
        {"first_name": "Michael", "last_name": "Johnson", "email": "michael.johnson@example.com"},
        {"first_name": "Emily", "last_name": "Williams", "email": "emily.williams@example.com"},
        {"first_name": "David", "last_name": "Brown", "email": "david.brown@example.com"},
        {"first_name": "Sarah", "last_name": "Jones", "email": "sarah.jones@example.com"},
        {"first_name": "James", "last_name": "Garcia", "email": "james.garcia@example.com"},
        {"first_name": "Lisa", "last_name": "Martinez", "email": "lisa.martinez@example.com"},
        {"first_name": "Robert", "last_name": "Rodriguez", "email": "robert.rodriguez@example.com"},
        {"first_name": "Maria", "last_name": "Hernandez", "email": "maria.hernandez@example.com"},
        {"first_name": "William", "last_name": "Lopez", "email": "william.lopez@example.com"},
        {"first_name": "Jennifer", "last_name": "Gonzalez", "email": "jennifer.gonzalez@example.com"},
        {"first_name": "Richard", "last_name": "Wilson", "email": "richard.wilson@example.com"},
        {"first_name": "Patricia", "last_name": "Anderson", "email": "patricia.anderson@example.com"},
        {"first_name": "Thomas", "last_name": "Thomas", "email": "thomas.thomas@example.com"},
        {"first_name": "Linda", "last_name": "Taylor", "email": "linda.taylor@example.com"},
        {"first_name": "Charles", "last_name": "Moore", "email": "charles.moore@example.com"},
        {"first_name": "Barbara", "last_name": "Jackson", "email": "barbara.jackson@example.com"},
        {"first_name": "Daniel", "last_name": "Martin", "email": "daniel.martin@example.com"},
        {"first_name": "Nancy", "last_name": "Lee", "email": "nancy.lee@example.com"}
    ]
    
    addresses_data = [
        {"street": "123 Main Street", "city": "New York", "state": "NY", "postal_code": "10001"},
        {"street": "456 Oak Avenue", "city": "Los Angeles", "state": "CA", "postal_code": "90001"},
        {"street": "789 Pine Road", "city": "Chicago", "state": "IL", "postal_code": "60601"},
        {"street": "321 Elm Street", "city": "Houston", "state": "TX", "postal_code": "77001"},
        {"street": "654 Maple Drive", "city": "Phoenix", "state": "AZ", "postal_code": "85001"},
        {"street": "987 Cedar Lane", "city": "Philadelphia", "state": "PA", "postal_code": "19101"},
        {"street": "147 Birch Court", "city": "San Antonio", "state": "TX", "postal_code": "78201"},
        {"street": "258 Spruce Way", "city": "San Diego", "state": "CA", "postal_code": "92101"},
        {"street": "369 Willow Path", "city": "Dallas", "state": "TX", "postal_code": "75201"},
        {"street": "741 Ash Boulevard", "city": "San Jose", "state": "CA", "postal_code": "95101"},
        {"street": "852 Poplar Street", "city": "Austin", "state": "TX", "postal_code": "73301"},
        {"street": "963 Cherry Avenue", "city": "Jacksonville", "state": "FL", "postal_code": "32099"},
        {"street": "159 Magnolia Drive", "city": "Fort Worth", "state": "TX", "postal_code": "76101"},
        {"street": "357 Hickory Road", "city": "Columbus", "state": "OH", "postal_code": "43004"},
        {"street": "486 Sycamore Lane", "city": "Charlotte", "state": "NC", "postal_code": "28201"},
        {"street": "792 Walnut Court", "city": "San Francisco", "state": "CA", "postal_code": "94101"},
        {"street": "135 Beech Street", "city": "Indianapolis", "state": "IN", "postal_code": "46201"},
        {"street": "246 Chestnut Way", "city": "Seattle", "state": "WA", "postal_code": "98101"},
        {"street": "579 Redwood Path", "city": "Denver", "state": "CO", "postal_code": "80201"},
        {"street": "681 Cypress Avenue", "city": "Boston", "state": "MA", "postal_code": "02101"}
    ]
    
    cars_data = [
        {"brand": "Toyota", "model": "Camry", "manufactured_year": "2022", "status": "active"},
        {"brand": "Honda", "model": "Civic", "manufactured_year": "2021", "status": "active"},
        {"brand": "Ford", "model": "F-150", "manufactured_year": "2023", "status": "maintenance"},
        {"brand": "Chevrolet", "model": "Silverado", "manufactured_year": "2022", "status": "active"},
        {"brand": "Tesla", "model": "Model 3", "manufactured_year": "2023", "status": "active"},
        {"brand": "BMW", "model": "X5", "manufactured_year": "2021", "status": "active"},
        {"brand": "Mercedes", "model": "C-Class", "manufactured_year": "2022", "status": "maintenance"},
        {"brand": "Audi", "model": "A4", "manufactured_year": "2023", "status": "active"},
        {"brand": "Nissan", "model": "Altima", "manufactured_year": "2020", "status": "active"},
        {"brand": "Mazda", "model": "CX-5", "manufactured_year": "2022", "status": "active"},
        {"brand": "Volkswagen", "model": "Jetta", "manufactured_year": "2021", "status": "maintenance"},
        {"brand": "Subaru", "model": "Outback", "manufactured_year": "2023", "status": "active"},
        {"brand": "Hyundai", "model": "Elantra", "manufactured_year": "2022", "status": "active"},
        {"brand": "Kia", "model": "Sportage", "manufactured_year": "2021", "status": "active"},
        {"brand": "Jeep", "model": "Wrangler", "manufactured_year": "2023", "status": "maintenance"},
        {"brand": "Ram", "model": "1500", "manufactured_year": "2022", "status": "active"},
        {"brand": "GMC", "model": "Sierra", "manufactured_year": "2023", "status": "active"},
        {"brand": "Lexus", "model": "RX 350", "manufactured_year": "2021", "status": "active"},
        {"brand": "Acura", "model": "MDX", "manufactured_year": "2022", "status": "maintenance"},
        {"brand": "Volvo", "model": "XC90", "manufactured_year": "2023", "status": "active"}
    ]
    
    # Insert 20 users with addresses and cars
    created_users = []
    for i in range(20):
        # Insert user
        user = db.insert("User", **users_data[i])
        created_users.append(user)
        
        # Insert address for user
        db.insert("Address", 
                  street=addresses_data[i]["street"],
                  city=addresses_data[i]["city"],
                  state=addresses_data[i]["state"],
                  postal_code=addresses_data[i]["postal_code"],
                  country="USA",
                  user_id=user.id)
        
        # Insert car for user
        db.insert("Car",
                  brand=cars_data[i]["brand"],
                  model=cars_data[i]["model"],
                  manufactured_year=cars_data[i]["manufactured_year"],
                  status=cars_data[i]["status"],
                  user_id=user.id)
    
    users = db.get("user")
    addresses = db.get("address")
    cars = db.get("car")
    lines = 100
    print("="*lines)
    for user in users:
        print(user)
    print("="*lines)
    for address in addresses:
        print(address)
    print("="*lines)
    for car in cars:
        print(car)
    print("="*lines)
    db.close()