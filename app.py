from enum import unique
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#init db
db = SQLAlchemy(app)
#init marshmallow
ma = Marshmallow(app)

#Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), unique=True)
    lastname = db.Column(db.String(200))
    email = db.Column(db.String(255), unique=True)
    dob = db.Column(db.String(20))

    def __init__(self, firstname, lastname, email, dob):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.dob = dob

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname', 'email', 'dob')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

#Add a new student
@app.route('/student', methods=['POST'])
def add_product():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    dob = request.json['dob']

    new_student = Student(firstname, lastname, email, dob)
    db.session.add(new_student)
    db.session.commit()

    return student_schema.jsonify(new_student)

#Get all students
@app.route("/student", methods=['GET'])
def get_products():
    all_students = Student.query.all()
    results = students_schema.dump(all_students)
    return jsonify(results)

#Get one student
@app.route("/student/<id>", methods=['GET'])
def get_product(id):
    student = Student.query.get(id)
    return student_schema.jsonify(student)

#Update Student details
@app.route('/student/<id>', methods=['PUT'])
def update_product(id):
    student = Student.query.get(id)
    #getting from user
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    dob = request.json['dob']

    #Init items to be commited
    student.firstname = firstname
    student.lastname = lastname
    student.email = email
    student.dob = dob

    db.session.commit()

    return student_schema.jsonify(student)

#remove a student from the database
@app.route("/student/<id>", methods=['DELETE'])
def delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()

    return student_schema.jsonify(student)


if __name__ == '__main__':
    app.run()