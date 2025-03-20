from data import (write_student_info, load_csv_as_dict,
                  load_as_csv, export_csv_records,
                  import_csv_records)


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


def print_student_info(student_records):
    print("\n======================================\n")
    print("Student records: \n")
    if student_records is None:
        print("There are not records in the system.")
    else:
        print("\n--------------------------------------\n")
        for student_record in student_records:
            print(student_record)
    print("\n======================================\n")


def print_menu(menu):
    print(menu)