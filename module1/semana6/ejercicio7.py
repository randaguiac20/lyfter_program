"""
7. Cree una función que acepte una lista de números y retorne una lista con los números primos de la misma.
    1. [1, 4, 6, 7, 13, 9, 67] → [7, 13, 67]
    2. Tip 1: Investigue la logica matematica para averiguar si un numero es primo, y conviertala a codigo.
    No busque el codigo, eso no ayudaria.
    3. *Tip 2: Aquí hay que hacer varias cosas (recorrer la lista, revisar si cada numero es primo, y agregarlo a otra lista).
    Así que lo mejor es agregar **otra función** para revisar si el numero es primo o no.*
"""

def check_prime_numbers(number_list):
    prime_number = list()
    for number in number_list:
        if get_prime_number(number):
            prime_number.append(number)
    return prime_number


def get_prime_number(number):
    # We need to discard if there is a number 1
    # because 1 is never a prime number, in case
    # there is a 1 in the list
    if number != 1:
        # While investigating I found that to calculate the power
        # of a number we need to do it like this 5**2
        # but to get a close square root of a number it is done to the
        # power of 0.5
        _number = int(number ** 0.5)
        # To be able to check against from 2 to the result of
        # the square root of the number we need to loop over for that range
        # to find out if a number is prime by using the % modulus option
        for index_range in range(2, _number + 1):
            print(f"Index {index_range} - sqr root {_number} - number: {number}")
            if number % index_range == 0:
                print(f"No prime number: {number}")
                return False
        print(f"Prime number: {number}")
        return number


number_list = [1, 4, 6, 7, 13, 9, 67, 8]
print(number_list)
print(check_prime_numbers(number_list))




# Better way of doing this
# def is_prime(number):
#     # 1 or less is not prime
#     if number <= 1:
#         return False
#     # Check divisors up to the square root
#     for divisor in range(2, int(number ** 0.5) + 1):
#         if number % divisor == 0:
#             return False
#     return True

# def filter_prime_numbers(number_list):
#     return [num for num in number_list if is_prime(num)]

# number_list = [1, 4, 6, 7, 13, 9, 67, 8]
# print(filter_prime_numbers(number_list))  # → [7, 13, 67]
