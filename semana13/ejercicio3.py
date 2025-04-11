"""
3. Cree una clase de `User` que:
    - Tenga un atributo de `date_of_birth`.
    - Tenga un property de `age`.
    
    Luego cree un decorador para funciones que acepten un `User`
    como parámetro que se encargue de revisar si el `User` es mayor
    de edad y arroje una excepción de no ser así.
"""
from datetime import date


class User:
    def __init__(self, birth_date):
        self.birth_date = birth_date
        self.current_year = date.today().year

    @property
    def age(self):
        age = (self.current_year - self.birth_date.year -
               ((date.today().month, date.today().day) < 
                (self.birth_date.month, self.birth_date.day)))
        return age

def adult_only(func):
    def wrapper(user):
        print("\nValidating your age to make sure you can buy the concert ticket...")
        if user.age < 18:
            print(f"\nYour age is {user.age}.")
            raise ValueError("You are not an adult yet, your under 18 years old.")
        else:
            print(f"\nYour age is: {user.age}, please proceed with the purchase of your ticket.")
            print()
        return func(user)
    return wrapper

@adult_only
def buy_ticket(user):
    return user

user_birth_date = date(2008, 11, 17)
user = User(user_birth_date)
buy_ticket(user)
