"""
5. Cree un programa que le pida al usuario 10 números, y al final le 
   muestre todos los números que ingresó, seguido del numero ingresado más alto.
    1. Ejemplos:
    2. 86, 54, 23, 54, 67, 21, 2, 65, 10, 32 → [54, 86, 23, 54, 67, 21, 2, 65, 10, 32]. El más alto fue 86.
"""

greater_number = 0
number_list = list()

print("\nPlease enter 10 numbers.\n")
for index in range(0, 10):
    index += 1
    number = int(input(f"\n{index}. Enter number: "))
    number_list.append(number)
    if number > greater_number:
        greater_number = number

# Better way of doing it
# for i in range(10):
#     num = int(input(f"{i+1}. Enter number: "))
#     number_list.append(num)
#greater_number = max(number_list)
print(f"\nAll 10 numbers entered by the user: {number_list}")
print(f"\nGreater number is: {greater_number}\n")
