
def convert_int_to_list(number):
    numbers_list = list()
    while number != 0:
        _number = number % 10
        number = (number - _number) // 10
        numbers_list.insert(0, _number)
    return numbers_list

msg = "\nThis function will be converting an integer to a list (each number will be an element.)"
print(msg)
number = int(input("\nEnter a number: "))
print(f"\n{convert_int_to_list(number)}\n")

# Better way of doing it
# number = int(input("\nEnter a number: "))
# numbers_list = [int(d) for d in str(number)]
# print(f"\n{numbers_list}\n")

# def convert_int_to_list(number):
#     numbers_list = []
#     while number > 0:
#         numbers_list.append(number % 10)
#         number //= 10
#     return numbers_list[::-1]  # reverse at the end

# number = int(input("\nEnter a number: "))
# print(f"\n{convert_int_to_list(number)}\n")

