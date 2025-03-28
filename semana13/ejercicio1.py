"""
1. Cree un decorador que haga print de los parámetros
y retorne la función que decore.
"""


def print_decorator(func):
    def wrapper(*args):
        print("\nPrinting items: ")
        for arg in args:
            print(f"{arg} - {type(arg)}")
        return func(*args)
    return wrapper


@print_decorator
def show_item_type(*args):
    return args


show_item_type(1, "2", True, [])
