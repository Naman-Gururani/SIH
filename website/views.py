# views.py

    
from werkzeug.utils import secure_filename
import os
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .model import Student,Teacher,Institution,Project
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    # if current_user.is_authenticated:
    #     return render_template('student_login.html')
    # else:
        # flash('You must be logged in to view this page.')
    return render_template('index.html')


@views.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if current_user.role != 'student':
        flash('Only students can add projects.')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        project_name = request.form.get('project_name')
        readme_file = request.files['readme_file']

        # Save the uploaded file
        if readme_file:
            filename = secure_filename(readme_file.filename)
            readme_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            readme_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            readme_file_path = None

        # Add other fields as necessary

        new_project = Project(project_name=project_name, readme_file_path=readme_file_path, student_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()

        flash('Project added successfully!')
        return redirect(url_for('views.home'))

    return render_template('add_project.html')


@views.route('/verify_students', methods=['GET', 'POST'])
@login_required
def verify_students():
    if current_user.role != 'institution':
        flash('Only institutions can verify students.')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        student = Student.query.get(student_id)

        if student and student.institution_id == current_user.id:
            student.verified = True
            db.session.commit()
            flash('Student verification status updated successfully.')
        else:
            flash('Student not found.')

    # Get all unverified students for the current institution
    students = Student.query.filter_by(institution_id=current_user.id, verified=False).all()
    return render_template('verify_students.html', students=students)
    
@views.route('/institute_profile', methods=['GET', 'POST'])
@login_required
def institute_profile():
    
    if current_user.role != 'institution':
        flash('Only institutions can verify students.')
        print ("calledin")
        return redirect(url_for('views.home'))
    print ("called")
    print(current_user.id)
    return render_template('institute_profile.html')




