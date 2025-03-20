"""
1. Cree una clase de `Circle` con:
    1. Un atributo de `radius` (radio).
    2. Un método de `get_area` que retorne su área.
"""


class Circle:
    def __init__(self, radio):
        self.radio = radio
        
    def get_area(self):
        # Formula A = π r²
        area = 3.14 * (self.radio ** 2)
        return f"\nThe area is: {round(area, 2)}."

program_on = True

while program_on:
    radio = int(input("\nPlease enter the radio of the circle: "))
    circle_area = Circle(radio)
    print(circle_area.get_area())
    exit = input("\nWould like to continue or exit the program 'yes or no': ")
    if exit == 'yes' or exit == 'y':
        program_on = False
    else:
        print("\nYou did not enter the right option. Program will continue.\n")
        