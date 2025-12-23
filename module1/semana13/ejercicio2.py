"""
2. Cree un decorador que se encargue de revisar si todos 
los parámetros de la función que decore son números,
y arroje una excepción de no ser así.
"""

def data_type_decorator(func):
    def wrapper(*args):
        print("Printing items...")
        for arg in args:
            if isinstance(arg, int):
                print((f"\nValidating items: {arg}."))
                print((f"This item {arg} is an integer."))
            elif isinstance(arg, float):
                print((f"\nValidating items: {arg}."))
                print((f"This item {arg} is an float."))
            else:
                print((f"\nValidating this item: {arg}."))
                raise TypeError(f"This item {arg} is not an integer.")
        return func(*args)
    return wrapper


@data_type_decorator
def print_data(*args):
    return args

print_data(20, 23.5, "hello", {"1": 0})
