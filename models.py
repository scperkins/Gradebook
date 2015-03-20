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

'''
if __name__ == "__main__":
    
    #connect to the database
    database.connect()
    #create the tables
    database.create_tables([Student, Course, Professor, StudentCourse, ProfessorCourse])
    
    #add students
    sean = Student.create(first_name="Sean", middle_initial="C.", last_name=" Perkins", grad_year=date(2013,5,19), gpa=3.2)
    ethan = Student.create(first_name="Ethan", middle_initial="J", last_name="Eldridge", grad_year=date(2013,5,19), gpa=2.1)
    sean.save()
    ethan.save()

    #add professors
    jeanne = Professor.create(first_name="Jeanne", last_name="Douglas")
    jackie = Professor.create(first_name="Jackie",  last_name="Horton")
    jeanne.save()
    jackie.save()

    #add courses
    cs101 = Course.create(name="Python Programming", course_id=101, credits=3.0)
    cs120 = Course.create(name="Java Programming", course_id=120, credits=3.0)
    cs101.save()
    cs120.save()

    #add student/course relationships
    sean_course = StudentCourse.create(student = sean, course=cs101)
    ethan_course = StudentCourse.create(student = ethan, course=cs120)
    #add professor/course relationships
    jeanne_python = ProfessorCourse.create(professor=jeanne, course=cs101)
    jackie_java = ProfessorCourse.create(professor=jackie, course=cs120)
'''
