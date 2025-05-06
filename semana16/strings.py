"""
4. Cree una función que le de la vuelta a un string y lo retorne.
    1. Esto ya lo hicimos en iterables.
    2. “Hola mundo” → “odnum aloH”
"""

def reverse_string(string):
    if not isinstance(string, str):
      raise TypeError("Input must be a string")
    if len(string) == 0:
        return string
    if len(string) == 1:
        return string
    _string = ""
    for gnirts in range(len(string)-1, -1, -1):
        _string += string[gnirts]
    return _string

string = "Hello World"
print(reverse_string(string))
