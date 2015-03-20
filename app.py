from flask import Flask, g, request, render_template
from models import *
#import views

app = Flask(__name__)

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
    #if request.method == 'POST'
    return render_template('index.html')

def get_students():
    students= Student.select()

if __name__ == "__main__":
    app.run(debug=True)
