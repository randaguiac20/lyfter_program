"""
2. Cree un decorador que se encargue de revisar si todos 
los parámetros de la función que decore son números,
y arroje una excepción de no ser así.
"""

def data_type_decorator(func):
    def wrapper(*args):
        func(args)
        for arg in args:
            if isinstance(arg, str):
                print((f"\nValidating this item: {arg}."))
                raise TypeError(f"This item {arg} is not an integer.")
            if isinstance(arg, int):
                print((f"\nValidating this item: {arg}."))
                print((f"This item {arg} is an integer."))
         
    return wrapper


@data_type_decorator
def print_data(items):
    print("Printing items...")

print_data(20, "hello")
