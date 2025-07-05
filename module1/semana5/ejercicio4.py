"""
4. Cree un programa que elimine todos los números impares de una lista.
    Ejemplos:
    `my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]` → `[2, 4, 6, 8]`
"""

number_list = [11, 2, 3, 4, 5, 1, 11, 6, 7, 8, 9, 13]

for number in number_list[:]:
    print(number)
    if number % 2 == 1:
        number_list.remove(number)
# Better way
#even_numbers = [num for num in number_list if num % 2 == 0]
print(f"Even numbers only: {number_list}")


        