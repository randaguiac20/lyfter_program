import json
from data import write_student_info, convert_csv_to_dict, show_as_csv


def calculate_grade_average(grades, single_avg=False):
    students_avg_grade = {}
    if single_avg:
        average = len(grades)
        _grade = 0
        for grade in grades:
            _grade = grade + _grade
            grade_avg = _grade // average
        return grade_avg
    if single_avg is False:
        for kstudent, vgrades in grades.items():
            average = len(vgrades)
            _grade = 0
            for grade in vgrades:
                _grade = grade + _grade
            grade_avg = _grade // average
            students_avg_grade[kstudent] = grade_avg
        return students_avg_grade


def validated_top_three(all_grades_sorted, all_grades):
    all_grades = list(set(all_grades))
    all_grades.sort(reverse=True)
    all_grades = all_grades[:3]
    first_grades = []
    second_grades = []
    third_grades = []
    students = []
    for student_info in all_grades_sorted:
        for student, vgrade in student_info.items():
            for grade in all_grades:
                try:
                    if vgrade == all_grades[0] and student not in students:
                        students.append(student)
                        first_grades.append({student: vgrade})
                    if vgrade == all_grades[1] and student not in students:
                        students.append(student)
                        second_grades.append({student: vgrade})
                    if vgrade == all_grades[2] and student not in students:
                        students.append(student)
                        third_grades.append({student: vgrade})
                except IndexError:
                    print("")
    return first_grades,second_grades,third_grades


def get_grades_per_student(data):
    try:
        all_grades = []
        for _, grade in data.items():
            all_grades.append(grade)
            all_grades.sort()
        all_grades_sorted = []
        on_off = True
        students = []
        while on_off:
            for grade in all_grades:
                for kstudent, vgrade in data.items():
                    if vgrade == grade and kstudent not in students:
                        students.append(kstudent)
                        all_grades_sorted.insert(0, {kstudent: vgrade})
                        if len(students) == len(data):
                            on_off = False
        return all_grades_sorted, all_grades
    except AttributeError:
        print("")


def average_grade_among_students(data):
    try:
        tmp_data = data.copy()
        all_average_grade = []
        for kstudent, vstudent in tmp_data.items():
            for kgrade, vgrade in vstudent.items():
                if "grade" in kgrade:
                    all_average_grade.append(int(vgrade))
        average_among_all_grades = calculate_grade_average(all_average_grade, single_avg=True)
        all_grades = f"Average grade among all students is: {average_among_all_grades}"
        return all_grades
    except AttributeError:
        print("")


def get_grade_average_per_student(data):
    try:
        tmp_data = data.copy()
        average_grade_per_student = {} 
        for kstudent, vstudent in tmp_data.items():
            average_grade_per_student.update({kstudent: []})
            for kgrade, vgrade in vstudent.items():
                if "grade" in kgrade:
                    average_grade_per_student[kstudent].append(int(vgrade))
        students_avg_grade = calculate_grade_average(average_grade_per_student)
        return students_avg_grade
    except AttributeError:
        print("")


def read_students_info(format="csv"):
    if format == "csv":
        show_as_csv()
    if format == "dict":
        student_info = convert_csv_to_dict()
        return student_info


def validate_grade_input(grade, subject):
    _grade = False
    while _grade is False:
        if grade > 100 or grade < 0:
            print("\nA invalid grade was entered, grades above 100 or below 0 are not allowed.\n")
            grade = int(input(f"Please provide the grade for {subject}: "))
            _grade = False
        else:
            _grade = True
            return grade


def get_student_info():
    name = input("\nPlease provide the student name and last name: ")
    student_class = input("Please provide the class name, i.e 11b: ")
    subjects = ["spanish_grade", "english_grade", "history_grade", "science_grade"]
    student_info = {
        "name": name,
        "class": student_class,
        "spanish_grade": 0,
        "english_grade": 0,
        "history_grade": 0,
        "science_grade": 0
    }
    student_list = []
    counter = 0
    on_off = True
    while on_off:
        try:
            _grade = int(input(f"Please provide the grade for {subjects[counter]}: "))
            valid_grade = validate_grade_input(_grade, subjects[counter])
            student_info.update({subjects[counter]: valid_grade})
            counter += 1
            if counter == len(subjects):
                on_off = False
        except ValueError:
            print("\nPlease enter a valid number.\n")
    student_list.append(student_info)
    write_student_info(student_list)


def get_all_student_info():
    print_student_info()


def get_third_grades():
    try:
        student_info = read_students_info(format="dict")
        grade_average = get_grade_average_per_student(student_info)
        all_grades_sorted, all_grades = get_grades_per_student(grade_average)
        top_three = validated_top_three(all_grades_sorted, all_grades)
        print("\nTop 3 grades average per student: ")
        counter = 1
        for top in top_three:
            print(f"\nTop {counter} Student(s)")
            for student_info in [data for data in top]:
                for student, grade in student_info.items():
                    print(f"{student}: {grade}")
            counter = counter + 1
    except TypeError:
        print("")


def get_average_grade_among_all():
    student_info = read_students_info(format="dict")
    average_grade_among_all = average_grade_among_students(student_info)
    try:
        print("\n")
        print(len(average_grade_among_all)*"=")
        print(average_grade_among_all)
        print(len(average_grade_among_all)*"=")
    except TypeError:
        print()


def exit_program():
    print("\nExiting program.\n")
    return False


def print_student_info():
    print("\n======================================\n")
    print("Student records: ")
    print("\n--------------------------------------\n")
    read_students_info(format="csv")
    print("\n--------------------------------------\n")
    print("======================================\n")


def print_menu(menu):
    print(menu)