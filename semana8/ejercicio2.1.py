"""
Cree un programa que me permita ingresar información de n cantidad de videojuegos y los guarde en un archivo csv.
Debe incluir:
    Nombre
    Género
    Desarrollador
    Clasificación ESRB
        E (Everyone): Apto para todas las edades, generalmente sin violencia ni contenido ofensivo.
        E10+ (Everyone 10 and older): Apto para niños de 10 años en adelante. Puede contener algo de violencia leve o lenguaje moderado.
        T (Teen): Apto para adolescentes de 13 años en adelante. Puede incluir violencia moderada, lenguaje más fuerte o sugerencias de contenido sexual.
        M (Mature): Apto para mayores de 17 años. Puede contener violencia intensa, lenguaje vulgar, contenido sexual o consumo de drogas.
        AO (Adults Only): Apto solo para adultos (18+), generalmente por contenido sexual explícito o violencia extrema.
        RP (Rating Pending): Se usa cuando un videojuego aún no ha sido clasificado por ESRB.
        Ejemplo de archivo final:
nombre,genero,desarrollador,clasificacion
Grand Theft Auto IV,Accion,Rockstar Games,M
The Elder Scrolls IV: Oblivion,RPG,Bethesda,M
Tony Hawk's Pro Skater 2,Deportes,Activision,T
"""
import csv
import os


def build_dataset(headers):
    dataset = {}
    data_list = []
    for subject_header in headers:
        _input = input(f"\nPlease provide the {subject_header} of the video game: ")
        dataset.update({subject_header: _input})
    data_list.append(dataset)
    return data_list

def create_and_write_csv_file(dataset, headers, filename="games_inventory.csv"):
    content = 0
    try:
        if os.path.getsize(filename):
            content = os.path.getsize(filename)
    except FileNotFoundError:
        content = 0
    with open(filename, 'a', encoding='utf-8') as file:
        csv_writter = csv.DictWriter(file, headers)
        if content == 0:
            csv_writter.writeheader()
            csv_writter.writerows(dataset)
        else:
            csv_writter.writerows(dataset)


def main():
    subject_headers = ["name", "type", "developer", "classification"]
    menu = """

This program will help you save the video information in a csv file.
    
    1. Enter new video game information.
    2. Exit the program.
"""
    program_on = True
    print(menu)
    while program_on:
        try:
            option = int(input("\nPlease choose an option from the menu i.e 1: "))
            if option > 2:
                print("\nERROR: You entered an invalid menu option.\n")
            elif option == 2:
                print("\nYou chose to close the program.")
                print("Thanks, we will see you again.\n")
                program_on = False
            else:
                dataset = build_dataset(subject_headers)
                create_and_write_csv_file(dataset=dataset, headers=subject_headers)
                print("\nDataset: \n")
                for data in dataset:
                    for key, value in data.items():
                        print(f"== {key}: {value}")
        except ValueError:
            print("\nERROR: You did not enter a number.\n")
        

if __name__ == "__main__":
    main()
