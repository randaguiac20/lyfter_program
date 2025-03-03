"""Cree un programa que le pida al usuario su nombre, apellido, y edad, 
y muestre si es un bebé, niño, preadolescente, adolescente, adulto joven,
adulto, o adulto mayor."""

name = input("Please enter your name: ")
lastname = input("Please enter your lastname: ")
age = int(input("Please enter your age: "))

if age <= 5:
    print("You are a baby!!")
elif age <= 11:
    print("You are a child!!")
elif age <= 14:
    print("You are a preteen!!")
elif age <= 18:
    print("You are a teenager")
elif age <= 26:
    print("You are a young adult")
elif age <= 59:
    print("You are an adult")
else:
    print("You are an older adult")
