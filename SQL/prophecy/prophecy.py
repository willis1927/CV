import csv
from cs50 import SQL


Input = []
with open ("students.csv", "r") as file:
    reader = csv.DictReader(file)
    for student in reader:
        Input.append(student)


Students = []
Houses = []
Relationships = []

for i in range(len(Input)):
    count = 0
    Students.append({"student_name" : Input[i]["student_name"]})
    for h in Houses:
        if h["house"] == Input[i]["house"]:
            count += 1
    if count == 0:
        Houses.append({"house" : Input[i]["house"],"head" : Input[i]["head"]})
    Relationships.append({"student_name" : Input[i]["student_name"],"house" : Input[i]["house"]})

db = SQL("sqlite:///roster.db")

for student in Students:
    db.execute("INSERT INTO new_students (student_name) VALUES (?)", student["student_name"])
for relation in Relationships:
    db.execute("INSERT INTO relationships (student_name, house) VALUES (?,?)", relation["student_name"],relation["house"])
for house in Houses:
    db.execute("INSERT INTO houses (house, head) VALUES (?,?)", house["house"], house["head"])
