"""
2. Cree un decorador que se encargue de revisar si todos 
los parámetros de la función que decore son números,
y arroje una excepción de no ser así.
"""

def data_type_decorator(func):
    def wrapper(*kwargs):
        print("Printing items...")
        for kwarg in kwargs:
            if isinstance(kwarg, int):
                print((f"\nValidating items: {kwarg}."))
                print((f"This item {kwarg} is an integer."))
            elif isinstance(kwarg, float):
                print((f"\nValidating items: {kwarg}."))
                print((f"This item {kwarg} is an float."))
            else:
                print((f"\nValidating this item: {kwarg}."))
                raise TypeError(f"This item {kwarg} is not an integer.")
        return func(*kwargs)
    return wrapper


@data_type_decorator
def print_data(*kwargs):
    return kwargs

print_data(20, 23.5, "hello", {"1": 0})
