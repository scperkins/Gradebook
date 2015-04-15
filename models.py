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
    gender = CharField(max_length=1)
    grad_year = DateField()
    gpa = FloatField()

class Professor(BaseModel):
    first_name = CharField(null=False)
    last_name = CharField(null=False)
    gender = CharField(max_length=1)

class Course(BaseModel):
    name = CharField()
    short_course_id = CharField()
    credits = FloatField()
    professor = ForeignKeyField(Professor, related_name = 'courses')

class Assignment(BaseModel):
    name = CharField(null=False)
    description = CharField()
    due_date = DateField()
    max_points = FloatField()

class StudentCourse(BaseModel):
    '''
    Specifies relationship between Student and Course
    '''
    student = ForeignKeyField(Student)
    course = ForeignKeyField(Course)

class AssignmentCourse(BaseModel):
    assignment = ForeignKeyField(Assignment)
    course = ForeignKeyField(Course)


