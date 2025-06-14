"""
3. Duplique el proyecto [Sistema de Control de Estudiantes]
   y modifíquelo para usar objetos para guardar 
   la información de los estudiantes (creando una clase de `Student`).
   	 1. Hay que cambiar los estudiantes de diccionarios a objetos.
     2. Hay que convertir la data del csv a un objeto en formato de diccionario al importar.
        (Read from exported file).
     3. Hay que convertir los objetos a diccionario al exportar a csv.
     4. Hay que modificar el acceso a los keys para accesar a atributos.
        1. student[’Name’] → student.name

BEFORE:

def create_student(students_list):
	name = input("Inserte su nombre: ")
	score = input("Inserte su nota: ")
	# (...)
	students_list.append({
		"name": name,
		"score": score,
		# (...)
	})

AFTER:

class Student():
	def __init__(self, name, score):
		self.name = name
		self.score = score
		# (...)

def create_student(students_list):
	name = input("Inserte su nombre: ")
	score = input("Inserte su nota: ")
	# (...)
	students_list.append(
		Student(name, score)
	)
"""

from student import StudentManager

menu = """

========================================================

This program will assist you with the student grades

1. Provide student information.
    a. Name.
    b. Class alphanumeric name.
    c. Spanish subject.
    d. English subject.
    e. History subject.
    f. Science subject.
    
2. Show list of students.
3. Show top 3 students with better grades.
4. Show average grade among all students.
5. See menu.
6. Export records in CSV format (Copy csv data to a new file).
7. Import records in CSV format (Read from exported file).
8. Exit the program.

"""

student_manager = StudentManager()

def show_menu():
    choices = {
        1: student_manager.set_student_info,
        2: student_manager.get_all_student_info,
        3: student_manager.get_top_third_grades,
        4: student_manager.get_average_grade_among_all,
        5: student_manager.print_menu,
        6: student_manager.export_records_as_csv,
        7: student_manager.import_records_as_csv,
        8: student_manager.exit_program
    }
    _result = ""
    program_on = True
    print(menu)
    while program_on:
        try:
            menu_option = int(input("\nPlease enter a menu option, i.e 1: "))
            if menu_option > 8:
                print("\nYou entered an option is not in the menu.\n")
            elif menu_option == 8:
                _result = choices.get(menu_option)
                program_on = _result()
            elif menu_option == 5:
                _result = choices.get(menu_option)
                _result(menu)
            else:
                _result = choices.get(menu_option)
                _result()
        except ValueError:
            print("\nYou have not entered a valid, option.")