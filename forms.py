# -*- coding: utf-8 -*-
"""
    :filename: forms.py
    :author: Sean Perkins <'github.com/scperkins'>
    :date: 3 May 2015
"""
from flask_wtf import Form
from wtforms import StringField, DateField, DecimalField, SelectField, TextAreaField, IntegerField, validators
from wtforms_components import TimeField

GENDER_CHOICE = [('M', 'Male'), ('F', 'Female')]

class StudentForm(Form):
    first_name = StringField("First Name", [validators.InputRequired()])
    middle_initial = StringField("Middle Initial", [validators.Length(max=1)])
    last_name = StringField("Last Name", [validators.InputRequired()])
    gender = SelectField(u'Gender', choices=GENDER_CHOICE)
    grad_year = DateField("Graduation Year", format='%Y-%m-%d')
    gpa = DecimalField("GPA", [validators.NumberRange(min=0, max=4.0)])


class ProfessorForm(Form):
    name = StringField("Name", [validators.InputRequired()])
    gender = SelectField("Gender", choices=GENDER_CHOICE)
    office = StringField("Office")
    hours_start = TimeField("Office Hours Start")
    hours_end = TimeField("Office Hours End")


class CourseForm(Form):
    name = StringField("Course Name", [validators.InputRequired()])
    short_course_id = StringField("Course ID")
    credits = DecimalField("Credits")
    professor = SelectField("Professor", coerce=int)


class AssignmentForm(Form):
    name = StringField("Assignment Name", [validators.InputRequired()])
    description = TextAreaField("Description")
    weight = DecimalField("Assignment Weight")
    due_date = DateField("Due Date", [validators.InputRequired()])
    max_points = DecimalField("Maximum Points", [validators.NumberRange(min=1)])


class GradeForm(Form):
    score = DecimalField("Score")
    comment = TextAreaField()
    student = SelectField("Student")
    assignment = SelectField("Assignment")
