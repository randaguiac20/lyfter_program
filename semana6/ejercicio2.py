"""
2. Experimente con el concepto de scope:
    1. Intente accesar a una variable definida dentro de una función desde afuera.
    2. Intente accesar a una variable global desde una función y cambiar su valor.
"""

global_var = "Scope = Global"
print(f"Outside - {global_var}")
def scope_local_var():
    local_var = "Scope = Local"
    print(local_var)
    
def scope_global_var():
    global_var = "A function changed me"
    print(f"Outside - {global_var}")

scope_global_var()
print(f"Local var: {local_var}")
scope_local_var()
