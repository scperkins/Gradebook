# -*- coding: utf-8 -*-
"""
    :filename: forms.py
    :author: Sean Perkins <'github.com/scperkins'>
    :date: 3 May 2015
"""
from flask_wtf import Form
from wtforms import StringField, DateField, DecimalField, SelectField,  validators

GENDER_CHOICE = [('M', 'Male'),('F', 'Female')]

class StudentForm(Form):
    first_name = StringField("First Name", [validators.InputRequired()])
    middle_initial = StringField("Middle Initial", [validators.Length(max=1)])
    last_name = StringField("Last Name", [validators.InputRequired()])
    gender = SelectField(u'Gender', choices=GENDER_CHOICE)
    grad_year = DateField("Graduation Year", format='%Y-%m-%d')
    gpa = DecimalField("GPA", [validators.NumberRange(min=0, max=4.0)])

class ProfessorForm(Form):
    first_name = StringField("First Name", [validators.InputRequired()])
    last_name = StringField("Last Name", [validators.InputRequired()])
    gender = SelectionField("Gender", choices=GENDER_CHOICE)
