from peewee import * 
from datetime import date

DATABASE = 'gradebook.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class Student(BaseModel):
    first_name = CharField(null=False)
    middle_initial = CharField()
    last_name = CharField(null=False)
    grad_year = DateField()
    gpa = FloatField()

class Course(BaseModel):
    name = CharField()
    short_course_id = CharField()
    credits = FloatField()

class Assignment(BaseModel):
    name = CharField(null=False)
    description = CharField()
    due_date = DateField()
    max_points = FloatField()

class Professor(BaseModel):
    first_name = CharField(null=False)
    last_name = CharField(null=False)

class ProfessorCourse(BaseModel):
    professor = ForeignKeyField(Professor)
    course = ForeignKeyField(Course)

class StudentCourse(BaseModel):
    student = ForeignKeyField(Student)
    course = ForeignKeyField(Course)


