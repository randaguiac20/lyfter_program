"""
1. Investigue cómo leer y escribir archivos `JSON` en Python [aquí](https://www.w3schools.com/python/python_json.asp).
2. Cree un programa que permita agregar un Pokémon nuevo al archivo
   de la lección de JSON ([Archivos JSON](https://www.notion.so/Archivos-JSON-79f9758cb59d4452a9c8668efa25356c?pvs=21)).
    1. Debe leer el archivo para importar los Pokémones existentes.
    2. Luego debe pedir la información del Pokémon a agregar.
    3. Finalmente debe guardar el nuevo Pokémon en el archivo.
"""
from pprint import pprint
import json


def open_file(filename="pokemon_inventory.json"):
    with open(filename, 'r') as file:
        _file = json.loads(file.read())
    return _file


def extract_json_structure(headers):
    clean_dataset = {}
    for key in headers[0].keys():
        if isinstance(headers[0][key], dict):
            clean_dataset.update({key: {}})
        if isinstance(headers[0][key], list):
            clean_dataset.update({key: []})
    return clean_dataset


def save_new_pokemon(data, dataset, filename="pokemon_inventory.json"):
    with open(filename, "w", encoding='utf-8') as file:
        data.append(dataset)
        file.write(json.dumps(data, indent=2))
    return data


def build_dataset(headers):
    clean_dataset = extract_json_structure(headers)
    for key, value in headers[0].items():
        for vk in value:
            if isinstance(value, dict):
                if key == "name":
                    _input = input(f"\nPlease provide the pokemon {key}: ")
                else:
                    _input = input(f"\nPlease provide the pokemon {vk}: ")
                clean_dataset[key].update({vk: _input})
            if isinstance(value, list):
                _input = input(f"\nPlease provide the pokemon {key}: ")
                clean_dataset.update({key: [_input]})
    print(50*"=")
    return clean_dataset


def main():
    menu = """
This program will help you create a pokemon character.
    
    1. Create your pokemon.
    2. Exit the program.
"""
    program_on = True
    print(menu)
    while program_on:
        try:
            print(50*"=")
            option = int(input("\nPlease choose an option from the menu i.e 1: "))
            if option > 2:
                print("\nERROR: You entered an invalid menu option.\n")
            elif option == 2:
                print("\nYou chose to close the program.")
                print("Thanks, we will see you again.\n")
                program_on = False
            else:
                data = open_file()
                dataset = build_dataset(headers=data)
                pprint(save_new_pokemon(data, dataset))
        except ValueError:
            print("\nERROR: You did not enter a number.\n")        


if __name__ == "__main__":
    main()
