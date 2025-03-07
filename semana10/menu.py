from actions import (get_student_info, get_all_student_info,
                     get_third_grades, get_average_grade_among_all,
                     exit_program, print_menu)


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
6. Exit the program.

"""

def show_menu():
    choices = {
        1: get_student_info,
        2: get_all_student_info,
        3: get_third_grades,
        4: get_average_grade_among_all,
        5: print_menu,
        6: exit_program
    }
    _result = ""
    program_on = True
    print(menu)
    while program_on:
        try:
            menu_option = int(input("\nPlease enter a menu option, i.e 1: "))
            if menu_option > 6:
                print("\nYou entered an option is not in the menu.\n")
            elif menu_option == 6:
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