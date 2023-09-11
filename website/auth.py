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

        if student:
            if not student.verified:
                flash('Verification pending from institution.')
                return redirect(url_for('auth.login_student'))

            if check_password_hash(student.password, password):
                login_user(student)
                return redirect(url_for('views.home'))

        flash('Invalid username or password')

    return render_template('login_student.html')

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

    return render_template('login_teacher.html')


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

    return render_template('login_institution.html')



# Student Sign_up
@auth.route('/signup_student', methods=['GET', 'POST'])
def signup_student():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        institution_name = request.form.get('institution_name')  # Get the institution name from the form
        name = request.form.get('name')
        gender = request.form.get('gender')
        address = request.form.get('address')
        country = request.form.get('country')
        dob = request.form.get('dob')

        student = Student.query.filter_by(email=email).first()

        if student:
            flash('Email already exists.')
            return redirect(url_for('auth.signup_student'))

        institution = Institution.query.filter_by(name=institution_name).first()
        if not institution:
            flash('Institution not found.')
            return redirect(url_for('auth.signup_student'))

        new_student = Student(email=email, password=generate_password_hash(password, method='sha256'), name=name, institution_id=institution.id, gender=gender, address=address, country=country, dob=dob)
        db.session.add(new_student)
        db.session.commit()

        flash('Account created!')
        return redirect(url_for('auth.login_student'))

    return render_template('signup_student.html')


# Teacher Sign up
@auth.route('/signup_teacher', methods=['GET', 'POST'])
def signup_teacher():
    # Similar to signup_student
    # ...
    pass


# Institution sign_up
@auth.route('/signup_institution', methods=['GET', 'POST'])
def signup_institution():
    # Similar to signup_student
    # ...
    pass

# @auth.route('/index',methods=['GET','POST'])
# def home():
#     if request.method=='POST':
#         # Handle POST Request here
#         return render_template('index.html')
#     return render_template('index.html')
