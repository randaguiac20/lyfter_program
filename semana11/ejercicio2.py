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
    def __init__(self, cls):
        self.max_passenger = 5
        self.seats = random.sample(range(1, 1001), 1000)
        self.exceed_passengers = f"\nSorry, No more passenger are allowed. ONLY {self.max_passenger}"
        self.person = cls

    def counter(self, action, counter):
        if self.max_passenger <= counter:
            return False
        if action == "add":
            counter += 1
            return True
        if action == "remove" and counter == 0:
            counter = 0
            return True
        if action == "remove" and counter > 0:
            counter -= 1
            return True
    
    def add_passenger(self, seat, passenger_list, passenger_info):
        true_false = self.counter("add", counter)
        if true_false:
            passenger_list.append(passenger_info)
            self.passengers = passenger_list
            print(f"\nPassenger: {self.person.name} - seat: {seat} -  get on the bus.")
        if true_false is False:
            print(self.exceed_passengers)
    
    def remove_passenger(self, counter, passenger_list, passenger_name):
        if len(passenger_list) == 0:
            print("\nNo passengers on board.")
        if len(passenger_list) != 0:
            for index, passenger in enumerate(passenger_list[:]):
                for name, seat in passenger.items():
                    if passenger_name == name:
                        passenger_list.pop(index)
                        self.counter("remove", counter)
                        return f"\nPassenger name: {passenger_name} - seat: {seat} -  get down the bus."
            return f"\nPassenger name: {passenger_name} was not found on this bus."
            
    def get_passengers(self, passenger_list):
        if len(passenger_list) == 0:
            print("\nNo passengers on board.\n")
            return False
        if len(passenger_list) != 0:
            print("\nPassengers on board are: \n")
            for passenger in passenger_list:
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
passenger_list = []
passenger_dict = {}
_menu = Menu(menu)
_menu.print_menu()

while program_on:
    try:
        option = _menu.get_menu_option()
        menu_option = _menu.menu_options(option)
        #passenger = Bus
        if menu_option == "add":
            passenger_name = input("\nPlease enter passenger name: ")
            passenger = Bus(Person(passenger_name))
            menu_counter = passenger.counter(menu_option, counter)
            passenger_dict = {passenger.person.name: passenger.seats[counter]}
            passenger.add_passenger(passenger.seats[counter], passenger_list, passenger_dict)
        if menu_option == "remove":
            on_board_passengers = passenger.get_passengers(passenger_list)
            if on_board_passengers is False:
                pass
            if on_board_passengers:
                passenger_name = input("\nPlease enter passenger name: ")
                menu_counter = passenger.counter(menu_option, counter)
                print(passenger.remove_passenger(menu_counter, passenger_list, passenger_name))
        if menu_option == "show":
            passenger.get_passengers(passenger_list)
        if menu_option == "exit":
            program_on = False
            print("\nExiting program as requested!!\n")
        if menu_option == "print_menu":
            _menu.print_menu()
        if menu_option is None:
            print("\nThis option is not part of the choises in the menu.")
        try:
            counter = menu_counter
        except NameError:
            print()
    except ValueError:
        print("\nPlease enter a number.")
