"""3. Cree un programa con un numero secreto del 1 al 10. El programa no debe 
    cerrarse hasta que el usuario adivine el numero.
        
        Debe investigar cómo generar un número aleatorio distinto cada
        vez que se ejecute.
"""
    
import random

matched_magic_number = False
print("\nWelcome to our guessing game.\n")

while matched_magic_number is False:
    magic_number = random.randrange(0, 10, 1)
    number = int(input("Please guess the magic number between 1 and 10, enter a number: "))
    if magic_number == number:
        print("\nYou won! you guess our magic number\n")
        matched_magic_number = True
    else:
        print("\nYou did not guess our magic number, try again\n")
