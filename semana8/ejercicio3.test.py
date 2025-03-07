"""
1. Investigue cómo leer y escribir archivos `JSON` en Python [aquí](https://www.w3schools.com/python/python_json.asp).
2. Cree un programa que permita agregar un Pokémon nuevo al archivo
   de la lección de JSON ([Archivos JSON](https://www.notion.so/Archivos-JSON-79f9758cb59d4452a9c8668efa25356c?pvs=21)).
    1. Debe leer el archivo para importar los Pokémones existentes.
    2. Luego debe pedir la información del Pokémon a agregar.
    3. Finalmente debe guardar el nuevo Pokémon en el archivo.
"""

import json


def build_dataset(headers):
    clean_dataset = {}
    for key, value in headers[0].items():
        clean_dataset = {key: {}}
        for vk in value:
            if isinstance(value, dict):
                if key == "name":
                    _input = input(f"\nPlease provide the pokemon {key}: ")
                else:
                    _input = input(f"\nPlease provide the pokemon {vk}: ")
                clean_dataset[key].update({vk: _input})
            if isinstance(value, list):
                _input = input(f"\nPlease provide the pokemon {key}: ")
                clean_dataset[key] = [_input]
    return clean_dataset



if __name__ == "__main__":
    headers = [
        {
            "name": {
            "english": "Pikachu"
            },
            "type": [
            "Electric"
            ],
            "base": {
            "HP": 35,
            "Attack": 55,
            "Defense": 40,
            "Sp. Attack": 50,
            "Sp. Defense": 50,
            "Speed": 90
            }
        }
    ]
    print(build_dataset(headers))