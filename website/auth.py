#auth.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import Student,Teacher,Institution,Project
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth,db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user,LoginManager

auth = Blueprint('auth', __name__)



# Student Login
@auth.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        student = Student.query.filter_by(email=email).first()
        print("in")

        if student:
            if not student.verified:
                print("in2")
                flash('Verification pending from institution.')
                return redirect(url_for('auth.login_student'))

            if check_password_hash(student.password, password):
                print("in3")
                login_user(student)
                return redirect(url_for('views.home'))

        flash('Invalid username or password')
        print("in4")

    return render_template('student_login.html')

# Teacher Login
@auth.route('/login_teacher', methods=['GET', 'POST'])
def login_teacher():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        teacher = Teacher.query.filter_by(email=email).first()

        if teacher and check_password_hash(teacher.password, password):
            login_user(teacher)
            return redirect(url_for('views.home'))

        flash('Invalid username or password')

    return render_template('Faculty_login.html')


# Institution Login
@auth.route('/login_institution', methods=['GET', 'POST'])
def login_institution():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        institution = Institution.query.filter_by(email=email).first()

        if institution and check_password_hash(institution.password, password):
            login_user(institution)
            return redirect(url_for('views.home'))

        flash('Invalid username or password')

    return render_template('institute_login.html')



# Student Sign_up
@auth.route('/signup_student', methods=['GET', 'POST'])
def signup_student():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        registration_number = request.form.get('studentID')
        institution_name = request.form.get('institution_name')  # Get the institution name from the form
        gender = request.form.get('gender')
        address = request.form.get('address')
        country = request.form.get('country')
        dob = request.form.get('dob')

        student = Student.query.filter_by(email=email).first()
        if student:
            flash('Email already exists.')
            return redirect(url_for('auth.signup_student'))
        print(institution_name)
        institution = Institution.query.filter_by(name=institution_name).first()
        if not institution:
            print("called")
            flash('Institution not found.')
            return redirect(url_for('auth.signup_student'))

        new_student = Student(email=email, password=generate_password_hash(password, method='sha256'), name=name,registration_number = registration_number, institution_id=institution.id, gender=gender, address=address, dob=dob)
        db.session.add(new_student)
        db.session.commit()

        flash('Account created!')
        return redirect(url_for('auth.login_student'))

    return render_template('Student_signup.html')


# Teacher Sign up
@auth.route('/signup_teacher', methods=['GET', 'POST'])
def signup_teacher():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        registration_number = request.form.get('facultyID')
        institution_name = request.form.get('institute_name')
        # Add any additional form fields here

        teacher = Teacher.query.filter_by(email=email).first()
        if teacher:
            flash('Email already exists.')
            return redirect(url_for('auth.signup_teacher'))
        
        institution = Institution.query.filter_by(name=institution_name).first()
        if not institution:
            print("called")
            flash('Institution not found.')
            return redirect(url_for('auth.signup_teacher'))

        # Create a new Teacher object and add it to the database
        new_teacher = Teacher(email=email, password=generate_password_hash(password, method='sha256'), name=name,registration_number=registration_number,institution_id=institution.id)
        db.session.add(new_teacher)
        db.session.commit()

        flash('Account created!')
        return redirect(url_for('auth.login_teacher'))

    return render_template('faculty_signup.html')


# Institution sign_up
@auth.route('/signup_institution', methods=['GET', 'POST'])
def signup_institution():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        location = request.form.get('location')
        print(password)
        institution = Institution.query.filter_by(email=email).first()
        if institution:
            flash('Email already exists.')
            return redirect(url_for('auth.signup_institution'))

        new_institution = Institution(email=email, password=generate_password_hash(password, method='sha256'), name=name, location=location)
        db.session.add(new_institution)
        db.session.commit()

        flash('Account created!')
        return redirect(url_for('auth.login_institution'))

    return render_template('institute_signup.html')

# @auth.route('/index',methods=['GET','POST'])
# def home():
#     if request.method=='POST':
#         # Handle POST Request here
#         return render_template('index.html')
#     return render_template('index.html')
