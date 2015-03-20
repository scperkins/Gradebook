from peewee import * 
from datetime import date

DATABASE = 'gradebook.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class Student(BaseModel):
    first_name = CharField()
    middle_initial = CharField()
    last_name = CharField()
    grad_year = DateField()
    gpa = FloatField()

class Course(BaseModel):
    name = CharField()
    course_id = IntegerField()
    credits = FloatField()

class Professor(BaseModel):
    first_name = CharField()
    last_name = CharField()

class ProfessorCourse(BaseModel):
    professor = ForeignKeyField(Professor)
    course = ForeignKeyField(Course)

class StudentCourse(BaseModel):
    student = ForeignKeyField(Student)
    course = ForeignKeyField(Course)


