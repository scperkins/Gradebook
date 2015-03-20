from flask import Flask, g, request, render_template, flash, redirect, url_for
from models import *

SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def create_tables():
    database.connect()
    database.create_tables([Student, Course, Professor, StudentCourse, ProfessorCourse])

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

@app.route('/students/add', methods=['GET', 'POST'])
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

if __name__ == "__main__":
    app.run(debug=True)
