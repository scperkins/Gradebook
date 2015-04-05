from flask import Flask, g, request, render_template, flash, redirect, url_for, abort
from models import *

SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def create_tables():
    database.connect()
    database.create_tables([Student, Course, Professor, StudentCourse, ProfessorCourse])

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

@app.route('/students/add', methods=['GET','POST'])
def add_students():
    if request.method == 'POST':
        try:
            with database.transaction():
                student = Student.create(
                        first_name=request.form['first_name'],
                        middle_initial=request.form['middle_initial'],
                        last_name=request.form['last_name'],
                        grad_year=request.form['grad_year'],
                        gpa=request.form['gpa'])
            flash('Student sucessfully added!')
            return redirect(url_for('get_students'))
        
        except IntegrityError:
            flash('Something went wrong...')
    
    return render_template('add_students.html')

@app.route('/students/')
def get_students():
    students= Student.select()
    return render_template('students.html',students=students)

@app.route('/students/<student_id>')
def student_detail(student_id):
    student = get_object_or_404(Student, Student.id == student_id)
    return render_template('student.html', student=student)

@app.route('/students/<student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.get(Student.id == student_id)
    student.delete_instance()
    flash("Student deleted")
    return redirect(url_for('get_students'))

@app.route('/professors/')
def get_profs():
    profs = Professor.select()
    return render_template('professors.html', profs=profs)

@app.route('/professors/<professor_id>')
def professor_detail(professor_id):
    professor = get_object_or_404(Professor, Professor.id == professor_id)
    return render_template('professor.html', prof=professor)

@app.route('/professors/add', methods=['GET', 'POST'])
def add_prof():
    if request.method == 'POST':
        try:
            with database.transaction():
                prof = Professor.create(
                        first_name=request.form['first_name'],
                        last_name=request.form['last_name']
                )
            flash('Professor successfully added')
            return redirect(url_for('get_profs'))
        
        except IntegrityError:
            flash('Something went wrong...')
    return render_template('add_professor.html')

@app.route('/courses/')
def get_courses():
    courses = Course.select()
    return render_template('courses.html', courses=courses)

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        try:
            with database.transaction():
                course = Course.create(
                        name=request.form['name'],
                        course_id=request.form['course_id'],
                        credits=request.form['credits']
                )
                flash('Course successfully added')
                return redirect(url_for('get_courses'))
        except IntegrityError:
            flash('Something went wrong...')
    return render_template('add_course.html')

if __name__ == "__main__":
    app.run(debug=True)
