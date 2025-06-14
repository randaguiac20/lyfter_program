"""
2. Cree una clase abstracta de `Shape` que:
    1. Tenga los métodos abstractos de `calculate_perimeter` y `calculate_area`.
    2. Ahora cree las siguientes clases que hereden de `Shape` e implementen esos métodos: `Circle`, `Square` y `Rectangle`.
    3. Cada una de estas necesita los atributos respectivos para poder calcular el área y el perímetro.
"""
from abc import ABC, abstractmethod
import math


class Shape(ABC):
    
    @abstractmethod
    def calculate_perimeter(self):
        pass
    
    @abstractmethod
    def calculate_area(self):
        pass

   
class Circle(Shape):
    def __init__(self):
        self.pi = math.pi
        self.radio = int(input("\nProvide the radio: "))

    def calculate_perimeter(self):
        # P=2πr
        self.perimeter = round(2 * math.pi * self.radio, 3)
        print(f"\nThe perimeter of the circle is: {self.perimeter}.")
    
    def calculate_area(self):
        # A=πr^2
        self.area = round(math.pi * self.radio ** 2, 3)
        print(f"\nThe are of the circle is: {self.area}")


class Square(Shape):
    def __init__(self):
        self.length = int(input("\nProvide the length: "))

    def calculate_perimeter(self):
        # P=4L
        self.perimeter = 4 * self.length
        print(f"\nThe perimeter of the square is: {self.perimeter}.")
    
    def calculate_area(self):
        # A=L^2
        self.area = self.length ** 2
        print(f"\nThe are of the square is: {self.area}.")


class Rectangle(Shape):
    def __init__(self):
        self.length = int(input("\nProvide the length: "))
        self.width = int(input("\nProvide the width: "))
    
    def calculate_perimeter(self):
        # P=2(L+W)
        self.perimeter = 4 * self.length
        print(f"\nThe perimeter of the rectangle is: {self.perimeter}.")
    
    def calculate_area(self):
        # A=L×W
        self.area = self.length * self.width
        print(f"\nThe area of the rectangle is: {self.area}.")


class Menu:
    def __init__(self, menu):
         self.menu = menu

    def get_shape_menu(self):
        self.shape_option = int(input("\nPlease enter an option from the menu, i.e 1 - 5: "))
        return self.shape_option
    
    def get_formula_menu(self):
        self.formula_option = int(input("\nWould like to choose to calculate the perimeter or the area, select 1 or 2: "))
        return self.formula_option
    
    def shape_menu(self):
        try:
            menu_options = {
                1: "circle",
                2: "square",
                3: "rectangle",
                4: "print_menu",
                5: "exit"
                
            }
            return menu_options.get(self.shape_option)
        except ValueError:
            print("Please enter a number.")
            
    def formula_menu(self):
        try:
            menu_options = {
                1: "perimeter",
                2: "area"
            }
            return menu_options.get(self.formula_option)
        except ValueError:
            print("Please enter a number.")

    def get_shape_formula(self, shape):
        shape_selection = {
            "circle": {
                    "class": Circle
                },
            "square": {
                    "class": Square
                },
            "rectangle": {
                    "class": Rectangle
                }
        }
        shape = shape_selection[shape]["class"]
        return shape
    
    def print_menu(self):
        print(self.menu)


def main():
    program_on = True
    menu = """

Thanks for using our calculator to find the following:

Perimter of a shape (Circle, Square, Rectangle).
Area of a shape (Circle, Square, Rectangle).

    Please select an option:

    1. Circle shape.
        1. Find the perimeter.
        2. Find the area.
    2. Square shape.
        1. Find the perimeter.
        2. Find the area.
    3. Rectangle shape.
        1. Find the perimeter.
        2. Find the area.
    4. Print menu.
    5: Exit program


    """

    _menu = Menu(menu)
    _menu.print_menu()

    while program_on:
        try:
            _menu.get_shape_menu()
            _shape = _menu.shape_menu()
            if _shape == "print_menu":
                _menu.print_menu()
            if _shape == "exit":
                program_on = False
                print("\nExiting program as requested!!\n")
            if _shape is None:
                print("\nThis option is not part of the choises in the menu.")
            if _shape in ["circle", "square", "rectangle"]:
                _menu.get_formula_menu()
                _formula = _menu.formula_menu()
                shape = _menu.get_shape_formula(_shape)
                if _shape == "rectangle":
                    rectangle = shape()
                    if _formula == "perimeter":
                        rectangle.calculate_perimeter()
                    if _formula == "area":
                        rectangle.calculate_area()
                if _shape == "square":
                    square = shape()
                    if _formula == "perimeter":
                        square.calculate_perimeter()
                    if _formula == "area":
                        square.calculate_area()
                if _shape == "circle":
                    circle = shape()
                    if _formula == "perimeter":
                        circle.calculate_perimeter()
                    if _formula == "area":
                        circle.calculate_area()
        except ValueError:
            print("\nPlease enter a number.")


if __name__ == "__main__":
    main()
