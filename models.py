# -*- coding: utf-8 -*-
"""
    :filename: models.py
    :author: Sean Perkins '<github.com/scperkins>'
    :date: March 2015
    :modified: 4 May 2015
"""
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
    gpa = DoubleField()

class Professor(BaseModel):
    name = CharField(null=False)
    gender = CharField(max_length=1)
    office = CharField()
    hours_start = TimeField()
    hours_end = TimeField()

class Course(BaseModel):
    name = CharField()
    short_course_id = CharField()
    credits = DoubleField()
    professor = ForeignKeyField(Professor)

class Assignment(BaseModel):
    name = CharField(null=False)
    description = CharField()
    due_date = DateField()
    weight = DoubleField()
    max_points = DoubleField()
    course = ForeignKeyField(Course)

class Grade(BaseModel):
    score = DoubleField()
    comment = CharField()
    student = ForeignKeyField(Student)
    assignment = ForeignKeyField(Assignment)

class StudentCourse(BaseModel):
    '''
    Specifies relationship between Student and Course
    '''
    student = ForeignKeyField(Student)
    course = ForeignKeyField(Course)



