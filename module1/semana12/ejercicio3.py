"""
3. Investigue qué usos se le pueden dar a la herencia multiple y cree un ejemplo
"""

# https://www.datacamp.com/es/tutorial/python-inheritance

"""
>> Benefits of Inheritance  

Reusability: With inheritance, you can write code once in the parent class and reuse it in the child classes.
             Using the example, both FullTimeEmployee and Contractor can inherit a get_details() method from the parent class Employee.  

Simplicity: Inheritance models relationships clearly.
            A good example is the FullTimeEmployee class, which "is a" type of the parent class Employee.  

Scalability: It also allows you to add new functions or child classes without affecting the existing code.
             For example, we can easily add a new Intern class as a child class.  

>> Potential Limitations of Inheritance  

Complexity: This might not surprise you, but too many levels of inheritance can make the code hard to follow.
            For example, if Employee has too many child classes like Manager, Engineer, Intern, etc., it can become confusing.  

Dependency: Changes in a parent class can unintentionally affect all subclasses.
            If you modify Employee, for example, it might break FullTimeEmployee or Contractor.  

Misuse: Using inheritance when it’s not the best option can complicate designs.
        You wouldn’t want to create a solution where Car inherits from Boat just to reuse move(). That relationship doesn’t make sense.  


There are 3 types of inheritance

. Multilevel Inheritance

class A:
    pass

class B(A):
    pass

class C(B):
    pass


. Hierarchical Inheritance

class A:
    pass

class B(A):
    pass

class C(A):
    pass


. Hybrid Inheritance

class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass


"""

class Person:
    def __init__(self, name, id, status):
        self.name = name
        self.id = id
        self.status = status
        
    def get_information(self):
        return f"\nName: {self.name}.\nID: {self.id}.\nStatus: {self.status}."

class Skill:
    def __init__(self, skill):
        self.skill = skill
        
    def get_skill(self):
        return f"Skill: {self.skill}."

class Student(Person, Skill):
    def __init__(self, name, id, status, skill):
        self.name = name
        self.id = id
        self.status = status
        self.skill = skill

class Employee(Person, Skill):
    def __init__(self, name, id, status, skill):
        self.name = name
        self.id = id
        self.status = status
        self.skill = skill

class Player(Person, Skill):
    def __init__(self, name, id, status, skill):
        self.name = name
        self.id = id
        self.status = status
        self.skill = skill


# Example usage
student = Student("Samuel", "04-0198-0345", "Student", "Long term memory")
print(student.get_information())
print(student.get_skill())

employee = Employee("Pablo", "04-0234-0984", "Employee", "High Tolerance")
print(employee.get_information())
print(employee.get_skill())

player = Player("Ronaldo (Brazilian)", "08-0425-0921", "Soccer player", "Fast dribbling")
print(player.get_information())
print(player.get_skill())
print()
