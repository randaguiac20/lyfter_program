"""
2. Cree una clase de `Bus` con:
    1. Un atributo de `max_passengers`.
    2. Un método para agregar pasajeros uno por uno.
       Requerimientos:
        1. Que acepte como parámetro una instancia de la clase `Person` vista en la lección.
        2. Este solo debe agregar pasajeros si lleva menos de su máximo.
        3. Sino, debe mostrar un mensaje de que el bus está lleno.
    3. Un método para bajar pasajeros uno por uno (en cualquier orden).
"""
import random

class Person:
    def __init__(self, name):
        self.name = name

class Bus:
    def __init__(self):
        self.max_passenger = 5
        self.seats = random.sample(range(1, 1001), 1000)
        self.exceed_passengers = f"\nSorry, Only {self.max_passenger} passenger are allowed."
        self.passenger_list = []

    def counter(self):
        if self.max_passenger <= len(self.passenger_list):
            print(self.exceed_passengers)
            return False
        return True
    
    def add_passenger(self):
        self.person = Person(input("\nPlease enter passenger name: "))
        seat = 0 if len(self.passenger_list) == 0 else len(self.passenger_list)
        self.passenger_list.append({self.person.name: self.seats[seat]})
        print(f"\nPassenger: {self.person.name} - seat: {self.seats[seat]} -  get on the bus.")
    
    def remove_passenger(self, passenger_name):
        if len(self.passenger_list) == 0:
            print("\nNo passengers on board.")
        if len(self.passenger_list) != 0:
            for index, passenger in enumerate(self.passenger_list[:]):
                for name, seat in passenger.items():
                    if passenger_name == name:
                        self.passenger_list.pop(index)
                        return f"\nPassenger name: {passenger_name} - seat: {seat} -  get down the bus."
            return f"\nPassenger name: {passenger_name} was not found on this bus."
            
    def get_passengers(self):
        if len(self.passenger_list) == 0:
            print("\nNo passengers on board.\n")
            return False
        if len(self.passenger_list) != 0:
            print("\nPassengers on board are: \n")
            for passenger in self.passenger_list:
                for name, seat in passenger.items():
                    print(f"Passenger name: {name} - Seat number: {seat}")
            return True

class Menu:
    def __init__(self, menu):
         self.menu = menu

    def get_menu_option(self):
        option = int(input("\nPlease enter an option from the menu, i.e 1 - 5: "))
        return option

    def menu_options(self, option):
        try:
            menu_options = {
                1: "add",
                2: "remove",
                3: "show",
                4: "print_menu",
                5: "exit"
                
            }
            return menu_options.get(option)
        except ValueError:
            print("Please enter a number.")
        
    
    def print_menu(self):
        print(self.menu)

counter = 0
program_on = True
menu = """

Thanks for using our Awesome Bus Station

Please select an option:

1. Add passenger.
2. Remove passenger.
3. Show list of passengers.
4. Print menu.
5: Exit program


"""
_menu = Menu(menu)
_menu.print_menu()
passenger = Bus()

while program_on:
    try:
        option = _menu.get_menu_option()
        menu_option = _menu.menu_options(option)
        if menu_option == "add":
            counter = passenger.counter()
            if counter:
                passenger.add_passenger()
        if menu_option == "remove":
            on_board_passengers = passenger.get_passengers()
            if on_board_passengers is False:
                pass
            if on_board_passengers:
                passenger_name = input("\nPlease enter passenger name: ")
                print(passenger.remove_passenger(passenger_name))
        if menu_option == "show":
            passenger.get_passengers()
        if menu_option == "exit":
            program_on = False
            print("\nExiting program as requested!!\n")
        if menu_option == "print_menu":
            _menu.print_menu()
        if menu_option is None:
            print("\nThis option is not part of the choises in the menu.")
    except ValueError:
        print("\nPlease enter a number.")
