"""
<aside>
💪🏽 **Ejercicios**

1. Cree una calculadora por linea de comando. Esta debe de tener un número actual,
   y un menú para decidir qué operación hacer con otro número:
1. Suma
2. Resta
3. Multiplicación
4. División
5. Borrar resultado

Al seleccionar una opción, el usuario debe ingresar el nuevo número a sumar, restar, multiplicar, o dividir por el actual.
El resultado debe pasar a ser el nuevo numero actual.
Debe de mostrar mensajes de error si el usuario selecciona una opción invalida,
o si ingresa un número invalido a la hora de hacer la operación.
"""

def addition(previous_number=0, current_number=0):
    print("\nYou chose the addition.\n")
    current_number += previous_number
    return current_number


def subtraction(previous_number=0, current_number=0):
    print("\nYou chose the subtraction.\n")
    if previous_number <= current_number:
        current_number -= previous_number
        return current_number
    if previous_number >= current_number:
        previous_number -= current_number
        return previous_number


def multiplier(previous_number=0, current_number=0):
    print("\nYou chose the multiplier.\n")
    current_number *= previous_number
    return current_number


def division(previous_number=0, current_number=0):
    print("\nYou chose the division.\n")
    if previous_number <= current_number:
        current_number = current_number // previous_number
        return current_number
    if previous_number >= current_number:
        previous_number = previous_number // current_number
        return previous_number


def erase_result(number=0):
    print("\nYou chose the option to reset calculator to 0.\n")
    return number


def power_off():
    print("\nPowering off the calculator.\n")
    return False


def calculator():
    menu = """
================================================================

    Calculator options:

    '+' Addition.
    '-' Subtraction.
    '*' Multiplier.
    '/' Division.
    'ac' Erase result.
    'off' Power off calculator.

"""
    calculator_on = True
    previous_number = 0
    while calculator_on:
        try:
            print(menu)
            _menu_dict = {
                    '+': addition,
                    '-': subtraction,
                    '*': multiplier,
                    '/': division,
                    'ac': erase_result,
                    'off': power_off
                }
            option = input("Choose an option from the menu i.e +: ")
            if option not in ("+", "-", "*", "/", "ac", "off"):
                print("\nYou entered an invalid option.\n")
                #raise Exception() ==> commented on purpose
            elif option == "ac":
                _calculator = _menu_dict.get(option)
                previous_number = _calculator()
            elif option == "off":
                _calculator = _menu_dict.get(option)
                calculator_on = _calculator()
            else:
                current_number = float(input("\nEnter a number: "))
                _calculator = _menu_dict.get(option)
                previous_number = _calculator(previous_number, current_number)
                print(f"\nFinal Result: {previous_number}")
        except ValueError:
            print("\nError: Please enter a number.\n")
            #raise ValueError() ==> commented on purpose


if __name__ == '__main__':
    try:
        calculator()
    except Exception:
        exit()
