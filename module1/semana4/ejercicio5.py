"""
5. Dada `n` cantidad de notas de un estudiante, calcular:
    1. Cuantas notas tiene aprobadas (mayor a 70).
    2. Cuantas notas tiene desaprobadas (menor a 70).
    3. El promedio de todas.
    4. El promedio de las aprobadas.
    5. El promedio de las desaprobadas.

"""

print("\nThis program will check if pass or fail as well as the average of pass, fail and all grades.\n")

counter = 0
amount_of_grades = int(input("Please enter the amount of grades: "))
pass_grades = 0
fail_grades = 0
avg_pass_grades = 0
avg_fail_grades = 0
all_avg_grades = 0

# Get the amount of passing and failing grades as well as their averages
while amount_of_grades != counter:
    counter = counter + 1
    grade = int(input("\nPlease provide your grade: "))
    if grade >= 70:
        pass_grades = pass_grades + 1
        avg_pass_grades = avg_pass_grades + grade
    else:
        fail_grades = fail_grades + 1
        avg_fail_grades = avg_fail_grades + grade

all_avg_grades = (avg_pass_grades + avg_fail_grades) // amount_of_grades

if pass_grades != 0:
    print(f"\nPassed grades: {pass_grades} with an average of {avg_pass_grades // pass_grades}")
else:
    print(f"\nNo passed grades.")

if fail_grades != 0:
    print(f"Failed grades: {fail_grades} with an average of {avg_fail_grades // fail_grades}")
else:
    print(f"\nNo failed grades.")

print(f"\nTotal average is {all_avg_grades}\n")        
