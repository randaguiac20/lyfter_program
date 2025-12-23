'''1. Experimente haciendo sumas entre distintos tipos de datos y apunte los resultados.
    1. Si le salen errores, **no se asuste.** Lealos e intente comprender qué significan.
    *Los errores son oportunidades de aprendizaje.*
    2. Por ejemplo:
        1. string + string → ?
        2. string + int → ?
        3. int + string → ?
        4. list + list → ?
        5. string + list → ?
        6. float + int → ?
        7. bool + bool → ?'''
        
print("hello " + "world")
"hello world"

#print("one" + 2)
"""Traceback (most recent call last):
  File "ejercicio1.py", line 14, in <module>
    print("one" + 2)
TypeError: can only concatenate str (not "int") to str"""

#print(2 + "one")
"""Traceback (most recent call last):
  File "ejercicio1.py", line 20, in <module>
    print(2 + "one")
TypeError: unsupported operand type(s) for +: 'int' and 'str'"""

#print([1] + [2])
"[1, 2]"

#print("one" + [2])
"""Traceback (most recent call last):
  File "ejercicio1.py", line 26, in <module>
    print("one" + [2])
TypeError: can only concatenate str (not "list") to str"""

#print(1.14 + 2)
"3.1399999999999997"

#print(True + False)
"1"