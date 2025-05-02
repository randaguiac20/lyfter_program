"""
3. Cree una función que retorne la suma de todos los números de una lista.
    1. La función va a tener un parámetro (la lista) y retornar un numero (la suma de todos sus elementos).
    2. [4, 6, 2, 29] → 41
"""

def add_numbers(number_list):
    result = 0
    for number in number_list:
        result += number
    return result

number_list = [4, 4, 6, 2, 29]
print(add_numbers(number_list))
