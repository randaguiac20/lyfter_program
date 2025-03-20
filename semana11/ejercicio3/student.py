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
from actions import (validate_grade_input, validated_top_three, get_grades_per_student,
                     get_grade_average_per_student, average_grade_among_students,
                     print_student_info)
from data import (write_student_info, load_as_csv, load_csv_as_dict,
                  export_csv_records, import_csv_records)


class Student():
    def __init__(self, name, s_class,
                 spanish_grade, english_grade,
                 history_grade, science_grade):
        self.name = name
        self.s_class = s_class
        self.spanish_grade = spanish_grade
        self.english_grade = english_grade
        self.history_grade = history_grade
        self.science_grade = science_grade

    def create_student(self):
        student_info = {
            "name": self.name,
            "class": self.s_class,
            "spanish_grade": self.spanish_grade,
            "english_grade": self.english_grade,
            "history_grade": self.history_grade,
            "science_grade": self.science_grade
        }
        self.student_data = student_info
        write_student_info(student_info)


class StudentManager():
    
    def set_student_info(self):
        student_info = {
                "name": input("Enter your name and lastname: "),
                "class": input("Enter your class i.e 11q: "),
                "spanish_grade": validate_grade_input(int(input("Enter your spanish grade: ")), "spanish"),
                "english_grade": validate_grade_input(int(input("Enter your english grade: ")), "english"),
                "history_grade": validate_grade_input(int(input("Enter your history grade: ")), "history"),
                "science_grade": validate_grade_input(int(input("Enter your science grade: ")), "science")
            }
        self.student = Student(student_info["name"], student_info["class"],
                        student_info["spanish_grade"], student_info["english_grade"],
                        student_info["history_grade"], student_info["science_grade"])
        self.student.create_student()

    def read_students_info(self, format="csv"):
        if format == "csv":
            student_info = load_as_csv()
            return student_info
        if format == "dict":
            student_info = load_csv_as_dict()
            return student_info

    def get_all_student_info(self):
        student_info = self.read_students_info()
        print_student_info(student_info)

    def _get_grade_average_per_student(self):
        self.grade_average = get_grade_average_per_student(self.read_students_info(format="dict"))
 
    def _get_grades_per_student(self):
        self.all_grades_sorted, self.all_grades = get_grades_per_student(self.grade_average)
        
    def _validated_top_three(self):
        self.top_three = validated_top_three(self.all_grades_sorted, self.all_grades)

    def get_top_third_grades(self):
        self._get_grade_average_per_student()
        self._get_grades_per_student()
        self._validated_top_three()
        print("\nTop 3 grades average per student: ")
        counter = 1
        for top in self.top_three:
            print(f"\nTop {counter} Student(s)")
            for student_info in [data for data in top]:
                for student, grade in student_info.items():
                    print(f"{student}: {grade}")
            counter = counter + 1
            
    def get_average_grade_among_all(self):
        student_info = self.read_students_info(format="dict")
        average_grade_among_all = average_grade_among_students(student_info)
        try:
            print("\n")
            print(len(average_grade_among_all)*"=")
            print(average_grade_among_all)
            print(len(average_grade_among_all)*"=")
        except TypeError:
            print()

    def export_records_as_csv(self):
        export_csv_records()


    def import_records_as_csv(self):
        student_info = import_csv_records()
        print_student_info(student_info)

    def exit_program(self):
        print("\nExiting program.\n")
        return False
    
    def print_menu(self, menu):
        print(menu)