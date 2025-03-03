"""
2. Cree un programa que cree un diccionario usando dos listas del mismo tamaño, 
   usando una para sus keys, y la otra para sus values.
    1. Ejemplos:
    2. `list_a = ["first_name", "last_name", "role"]`
    `list_b = ["Alek", "Castillo", "Software Engineer"]`
    → `{"first_name": "Alek", "last_name": "Castillo", "role": "Software Engineer"}`
"""


key_list = ["first_name", "last_name", "role"]
value_list = ["Alek", "Castillo", "Software Engineer"]
user_information = dict()

for index in range(0, len(key_list)):
    user_information[key_list[index]] = value_list[index]

print(user_information)
