# Requerimientos

Investigue sobre la biblioteca [FreeSimpleGUI](https://pypi.org/project/PySimpleGUI/)  y cree un programa **con interfaz gráfica** que permita la gestión de finanzas personales. Este debe mostrar:

- Una tabla de movimientos (gastos e ingresos).
- Un botón para agregar una categoría de movimiento.
    - Este botón debe abrir otra ventana para agregar esa categoría.
    - Por ejemplo: Comida, Familia, Carro, etc.
- Un botón para agregar un gasto.
    - Este botón debe abrir otra ventana para agregar ese gasto.
    - Los gastos deben tener un titulo, un monto y una categoría.
- Un botón para agregar un ingreso.
    - Este botón debe abrir otra ventana para agregar esa ingreso.
    - Los ingresos deben tener un titulo, un monto y una categoría.

Así mismo:

- Si yo intento agregar un ingreso o un gasto, pero no hay  ninguna categoría agregada previamente, debe mostrar un error que diga “Por favor ingrese una categoría antes”.
- Cada vez que haga cambios, se debe exportar la data automáticamente en archivos.
- Cada vez que yo abra el programa, debe importar la data automáticamente (si existe).
- Toda la lógica debe ir separada en módulos y funciones.