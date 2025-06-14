"""
1. Cree una clase de `BankAccount` que:
    1. Tenga un atributo de `balance`.
    2. Tenga un método para ingresar dinero.
    3. Tengo un método para retirar dinero.
    
    Cree otra clase que herede de esta llamada `SavingsAccount` que:
    
    1. Tenga un atributo de `min_balance` que se pueda asignar al crearla.
    2. Arroje un error si se intenta retirar dinero y si el `balance` está debajo del `min_balance`.
"""
from abc import ABC, abstractmethod


class BankAccount(ABC):
    def __init__(self, balance=0):
        # Balance is in dolars
        self.balance = balance
    
    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def deposit(self, amount):
        pass
    

class SavingsAccount(BankAccount):
    def __init__(self, balance, min_balance):
        self.balance = balance
        # Minimun balance is in dolares
        self.min_balance = min_balance

    def validate_widthdraw_balance(self, amount):
        subtraction = self.balance - amount
        if self.min_balance > subtraction:
            print(f"\n>> You are under the minimum balance {self.min_balance}$.")
            print(f"\n>> Your current balance is: {self.balance}$.")
        if self.balance < amount:
            print(f"\n>> There is not enough money in your account.")
            print(f"\n>> Your current balance is: {self.balance}$.")
        if self.min_balance <= subtraction:
            self.balance -= amount
            print(f"\nYou take out {amount}$ to your account. Your new balance is: {self.balance}$")

    def withdraw(self):
        # Get money out of my account
        if self.balance == 0:
            print(f"\n>> No enough money in your account!! Your current balance is: {self.balance}$.")
        if self.balance != 0:
            print(f"\nRemember the minimun amount in your account should be: {self.min_balance}$.")
            amount = int(input("\nPlease enter the amount you want to take out: "))
            self.validate_widthdraw_balance(amount)

    def deposit(self):
        amount = int(input("\nPlease enter the amount of your deposit: "))
        # Put money in my account
        self.balance += amount
        print(f"\nYou add {amount}$ to your account. Your new balance is: {self.balance}$")

    def get_balance(self):
        print(f"\nYour balance is: {self.balance}$")


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


program_on = True
menu = """

Welcome to the best Bank in the world WWW

Please select an option:

1. Make a Deposit.
2. Make a withdrawal.
3. Show my balance.
4. Print menu.
5: Exit program


"""
passenger_dict = {}
_menu = Menu(menu)
_menu.print_menu()
saving_account = SavingsAccount(balance=0, min_balance=10)

while program_on:
    try:
        option = _menu.get_menu_option()
        menu_option = _menu.menu_options(option)
        if menu_option == "add":
            saving_account.deposit()
        if menu_option == "remove":
            saving_account.withdraw()
        if menu_option == "show":
            saving_account.get_balance()
        if menu_option == "exit":
            program_on = False
            print("\nExiting program as requested!!\n")
        if menu_option == "print_menu":
            _menu.print_menu()
        if menu_option is None:
            print("\nThis option is not part of the choises in the menu.")
    except ValueError:
        print("\nPlease enter a number.")
