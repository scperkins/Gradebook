# -*- coding: utf-8 -*-
from flask import Flask, g, request, render_template, flash, redirect, url_for, abort
from models import *
from forms import *

SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def create_tables():
    database.connect()
    database.create_tables([Student, Course, Professor, Assignment, StudentCourse], safe=True)

def get_object_or_404(model, *expressions):
    try:
        return model.get(*expressions)
    except model.DoesNotExist:
        abort(404)

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

"""Students"""
@app.route('/students/add', methods=['GET','POST'])
def add_students():
    form = StudentForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            with database.transaction():
                Student.create(
                    first_name=form.first_name.data,
                    middle_initial=form.middle_initial.data,
                    last_name=form.last_name.data,
                    gender=form.gender.data,
                    grad_year=form.grad_year.data,
                    gpa=form.gpa.data)
            flash('Student successfully added!')
            return redirect(url_for('get_students'))
        
        except IntegrityError:
            flash('Something went wrong...')
    
    return render_template('add_students.html', form=form)

@app.route('/students/')
def get_students():
    students= Student.select()
    return render_template('students.html',students=students)

@app.route('/students/<int:student_id>')
def student_detail(student_id):
    student = get_object_or_404(Student, Student.id == student_id)
    return render_template('student.html', student=student)

@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    student = Student.get(Student.id == student_id)
    student.delete_instance()
    flash("Student deleted")
    return redirect(url_for('get_students'))

@app.route('/students/<int:student_id>/', methods=['GET','POST'])
def edit_student(student_id):
    student = Student.get(Student.id == student_id)
    form = StudentForm(request.form, obj=student)
    if request.method == 'POST' and form.validate():
        form.populate_obj(student)
        student.save()
        flash("Edit successful")
        return redirect(url_for('student_detail', student_id=student_id))
    return render_template('edit_student.html', student=student, form=form)

"""Professors"""
@app.route('/professors/')
def get_profs():
    profs = Professor.select()
    return render_template('professors.html', profs=profs)

@app.route('/professors/<int:professor_id>')
def professor_detail(professor_id):
    professor = get_object_or_404(Professor, Professor.id == professor_id)
    courses_taught = Course.select().where(Course.professor == professor_id)
    return render_template('professor.html', prof=professor, courses=courses_taught)

@app.route('/professors/add', methods=['GET', 'POST'])
def add_prof():
    form = ProfessorForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            with database.transaction():
                Professor.create(
                    name=form.name.data,
                    gender=form.gender.data,
                    office=form.office.data,
                    hours_start=form.hours_start.data,
                    hours_end=form.hours_end.data
                )
            flash('Professor successfully added')
            return redirect(url_for('get_profs'))
        
        except IntegrityError:
            flash('Something went wrong...')
    return render_template('add_professor.html', form=form)

@app.route('/professors/<int:professor_id>', methods=['GET', 'POST'])
def edit_professor(professor_id):
    professor = Professor.get(Professor.id == professor_id)
    form = ProfessorForm(request.form, obj=professor)
    if request.method == 'POST' and form.validate():
        form.populate_obj(professor)
        professor.save()
        flash('Edit on Professor {} was successful'.format(professor.name))
        return redirect(url_for('professor_detail', professor_id=professor_id))
    return render_template('edit_professor.html', professor=professor, form=form) 

@app.route('/professors/<int:professor_id>/delete', methods=['GET','POST'])
def delete_prof(professor_id):
    professor = Professor.get(Professor.id == professor_id)
    professor.delete_instance()
    flash("Professor Deleted")
    return redirect(url_for('get_profs'))

"""Courses/Assignments"""
@app.route('/courses/')
def get_courses():
    courses = Course.select()
    return render_template('courses.html', courses=courses)

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    form = CourseForm(request.form)
    form.professor.choices = [(prof.id, prof.name)
            for prof 
            in Professor.select().order_by(Professor.name.asc())]
    if request.method == 'POST':
        try:
            with database.transaction():
                course = Course.create(
                    name=form.name.data,
                    short_course_id=form.short_course_id.data,
                    credits=form.credits.data,
                    professor=form.professor.data
                )
            flash('{} successfully added'.format(course.name))
            return redirect(url_for('get_courses'))
        except IntegrityError:
            flash('Something went wrong...')
    return render_template('add_course.html', form=form)

@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = get_object_or_404(Course, Course.id == course_id)
    assignments = Assignment.select().where(Assignment.course == course_id)
    return render_template('course.html', course=course, assignments=assignments)

@app.route('/courses/<int:course_id>/', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.get(Course.id == course_id)
    form = CourseForm(request.form, obj=course)
    form.professor.choices = [(prof.id, prof.name)
            for prof
            in Professor.select().order_by(Professor.name.asc())]
    if request.method == 'POST':
        form.populate_obj(course)
        course.save()
        flash('Changes to {} were saved.'.format(course.name))
        return redirect(url_for('course_detail', course_id=course.id))
    return render_template('edit_course.html', form=form, course=course)

@app.route('/courses/<int:course_id>/add_assignment', methods=['GET', 'POST'])
def add_assignment(course_id):
    course = get_object_or_404(Course, Course.id == course_id)
    form = AssignmentForm(request.form, obj=course)
    if request.method == 'POST':
        try:
            with database.transaction():
                Assignment.create(
                    name=form.name.data,
                    description=form.description.data,
                    due_date=form.due_date.data,
                    max_points=form.max_points.data,
                    course=course
                )
            flash('Assignment successfully added to {}'.format(course.name))
            return redirect(url_for('course_detail', course_id=course.id))
        except IntegrityError:
            flash('Something went wrong...')
    return render_template('add_assignment.html', course=course, form=form)

@app.route('/assignment/<int:assign_id>', methods=['GET', 'POST'])
def assignment(assign_id):
    assignment = get_object_or_404(Assignment, Assignment.id == assign_id)
    return render_template('assignment.html', assignment=assignment)

@app.route('/assignment/<int:assign_id>/', methods=['GET', 'POST'])
def edit_assignment(assign_id):
    assignment = Assignment.get(Assignment.id == assign_id)
    form = AssignmentForm(request.form, obj=assignment)
    if request.method == 'POST':
        form.populate_obj(assignment)
        assignment.save()
        flash("Changes were saved to assignment: {}".format(assignment.name))
        return redirect(url_for('assignment', assign_id=assign_id))
    return render_template('edit_assignment.html', form=form, assignment=assignment)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
