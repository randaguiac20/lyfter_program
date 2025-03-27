"""
1. Cree un decorador que haga print de los parámetros
y retorne la función que decore.
"""


def print_decorator(func):
    def wrapper(*args):
        func(args)
    return wrapper


@print_decorator
def show_item_type(items):
    print()
    for item in items:
        print(f"Item: {item} - type: {type(item)}")
    print()
    

show_item_type(1, "2", True, [])
