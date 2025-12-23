"""
1. Cree una clase de `Circle` con:
    1. Un atributo de `radius` (radio).
    2. Un método de `get_area` que retorne su área.
"""
import math


program_on = True

def validate_answer():
    validate = True
    while validate:
        answer = input("\nWould like to continue or exit the program 'yes or no': ")
        if answer.lower() == 'yes' or answer.lower() == 'y':
            print("\nExcellent let's continue!!\n")
            program_on = True
            validate = False
        elif answer.lower() == 'no' or answer.lower() == 'n':
            print("\nExisting program!!\n")
            program_on = False
            validate = False
        else:
            print("\nYou did not enter the right option. Program will continue.\n")
    return program_on
        


class Circle:
    def __init__(self, radio):
        self.radio = radio
        
    def get_area(self):
        # Formula A = π r²
        area = math.pi * (self.radio ** 2)
        return f"\nThe area is: {round(area, 2)}."


while program_on:
    radio = int(input("\nPlease enter the radio of the circle: "))
    circle_area = Circle(radio)
    print(circle_area.get_area())
    program_on = validate_answer()

    
        