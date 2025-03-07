"""
6. Cree una función que acepte un string con palabras separadas por un guión
   y retorne un string igual pero ordenado alfabéticamente.
    1. Hay que convertirlo a lista, ordenarlo, y convertirlo nuevamente a string.
    2. “python-variable-funcion-computadora-monitor” → “computadora-funcion-monitor-python-variable”
"""

def order_words_alphabetically(statement):
    if "-" in statement:
        word_list = statement.split("-")
        word_list.sort()
        new_statement = "-".join(word_list)
        return new_statement
    else:
        return "You did not enter a string with a dash."
            
print("Provide a statement to order the words alphabetically ")
statement = input("Enter your statement with a dash i.e python-variable-funcion-computadora-monitor: ")
print(order_words_alphabetically(statement))
