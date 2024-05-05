# # =====================Inheritance===============================
#
# # ============creating parent class
# class Person(object):
#
#     def __init__(self, name, id):
#         self.name = name
#         self.id = id
#
#     def Display(self):
#         print(self.name, self.id)
#
#
# emp = Person("Rafsan", 102)
# emp.Display()
#
#
# #=================creating child class from parent============
# class Emp(Person):
#
#     def Print(self):
#         print("Emp class called")
#
#
# Emp_details = Emp("zamil", 103)
#
# # calling parent class function
# Emp_details.Display()
#
# # Calling child class function
# Emp_details.Print()
#
#
# #============Example of Inheritance
#
#
# class Student(object):
#
#     # Constructor
#     def __init__(self, name):
#         self.name = name
#
#     def getName(self):
#         return self.name
#
#     def isEmployee(self):
#         return False
#
#
# class Employee(Student):
#
#     def isEmployee(self):
#         return True
#
#
# emp = Student("Geek1")
# print(emp.getName(), emp.isEmployee())
#
# emp = Employee("Geek2")
# print(emp.getName(), emp.isEmployee())
#
#
# #==============calling constructor of parent class===========
#
# class Computer(object):
#
#     def __init__(self, name, idnumber):
#         self.name = name
#         self.idnumber = idnumber
#
#     def display(self):
#         print(self.name)
#         print(self.idnumber)
#
#
# # child class
# class Desktop(Computer):
#     def __init__(self, name, idnumber, price, model):
#         self.price = price
#         self.model = model
#
#         # invoking the __init__ of the parent class
#         Computer.__init__(self, name, idnumber)
#
#
# # creation of an object variable or an instance
# a = Desktop('Rahul', 886012, 200000, "i7")
#
# # calling a function of the class Person using its instance
# a.display()
#
#
# class A:
#     def __init__(self, n='Rahul'):
#         self.name = n
#
# class B(A):
#     def __init__(self, name,roll):
#         self.roll = roll
#
#         A.__init__(self,name)
#
#
# object = B('rahul',23)
# print(object.name)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
