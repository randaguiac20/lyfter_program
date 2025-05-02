"""
4. Cree una función que le de la vuelta a un string y lo retorne.
    1. Esto ya lo hicimos en iterables.
    2. “Hola mundo” → “odnum aloH”
"""

def reverse_string(string):
    _string = ""
    for gnirts in range(len(string)-1, -1, -1):
        _string += string[gnirts]
    return _string

string = "Hello World"
print(reverse_string(string))
