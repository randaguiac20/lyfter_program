"""
1. Cree un diccionario que guarde la siguiente información sobre un hotel:
    - `nombre`
    - `numero_de_estrellas`
    - `habitaciones`
- El value del key de `habitaciones` debe ser una lista, y cada habitación debe tener la siguiente información:
    - `numero`
    - `piso`
    - `precio_por_noche`
"""

hotel = {
    "nombre": "Hotel Vista de las flores",
    "numero_de_estrellas": 4,
    "habitaciones": [
        {
        "numero": 101,
        "piso": 1,
        "precio_por_noche": "1050$"        
    },
    {
        "numero": 102,
        "piso": 1,
        "precio_por_noche": "1000$"        
    },
    {
        "numero": 103,
        "piso": 1,
        "precio_por_noche": "1300$"        
    },
    {
        "numero": 104,
        "piso": 1,
        "precio_por_noche": "1000$"        
    },
    {
        "numero": 105,
        "piso": 1,
        "precio_por_noche": "1000$"        
    },
    {
        "numero": 106,
        "piso": 1,
        "precio_por_noche": "1500$"        
    }
    ]
}

print(f"Hotel: {hotel.get('nombre')}")
print(f"Stars: {hotel.get('numero_de_estrellas')}")
for room in hotel.get('habitaciones'):
    print("\nRoom information: ")
    for key, value in room.items():
        print(f"{key} - {value}")
