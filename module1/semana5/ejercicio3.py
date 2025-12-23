"""
3. Cree un programa que intercambie el primer y ultimo elemento de una lista.
   Debe funcionar con listas de cualquier tamaño.
    1. Ejemplos:
    2. `my_list = [4, 3, 6, 1, 7]` → `[7, 3, 6, 1, 4]`
"""

my_list = [20, 4, 3, 6, 1, 7, 12, 25]
print(f"Current list: {my_list}")
first_index = my_list.pop(0)
last_index = my_list.pop(-1)
# Intercambiar primero y último better way
#my_list[0], my_list[-1] = my_list[-1], my_list[0]
my_list.append(first_index)
my_list.insert(0, last_index)
print(f"Updated list: {my_list}")
