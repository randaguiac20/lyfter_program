"""
4. Cree un programa que le pida tres números al usuario y muestre el mayor.
"""

print("\nPlease enter 3 different numbers.\n")

n_1 = int(input("Please enter your first number: "))
n_2 = int(input("Please enter your second number: "))
n_3 = int(input("Please enter your third number: "))

if n_1 > n_2 and n_1 > n_3:
    print(f"\nFirst number {n_1} was the greater number.\n")
if n_2 > n_1 and n_2 > n_3:
    print(f"\nSecond number {n_2} was the greater number.\n")
if n_3 > n_1 and n_3 > n_2:
    print(f"\nThird number {n_3} was the greater number.\n")
