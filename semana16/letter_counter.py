"""
5. Cree una función que imprima el numero de mayúsculas y el numero de minúsculas en un string.
    1. “I love Nación Sushi” → “There’s 3 upper cases and 13 lower cases”
"""

def letter_case_counter(string):
    if not isinstance(string, str):
        raise TypeError("The input must be a string")
    if len(string) == 0:
        raise ValueError("The input string cannot be empty")
    upper_case = 0
    lower_case = 0
    msg = ""
    for letter in string:
        if letter.isupper() and not letter.isdigit():
            upper_case += 1
        if letter.islower() and not letter.isdigit():
            lower_case += 1
    if upper_case == 0 and lower_case == 0:
        print(f"There's {upper_case} upper case and {lower_case} lower case")
        msg = f"There's {upper_case} upper case and {lower_case} lower case"
    elif upper_case == 0 and lower_case > 0:
        print(f"There's {upper_case} upper case and {lower_case} lower cases")
        msg = f"There's {upper_case} upper case and {lower_case} lower cases"
    elif upper_case > 0 and lower_case == 0:
        print(f"There's {upper_case} upper cases and {lower_case} lower case")
        msg = f"There's {upper_case} upper cases and {lower_case} lower case"
    else:
        print(f"There's {upper_case} upper cases and {lower_case} lower cases")
        msg = f"There's {upper_case} upper cases and {lower_case} lower cases"
    return msg

string = "This is a test string with 2 numbers 123 and 3 letters"
letter_case_counter(string)
