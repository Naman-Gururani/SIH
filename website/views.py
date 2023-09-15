# views.py

    
from werkzeug.utils import secure_filename
import os
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user,logout_user
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

    return render_template('Project.html')



@views.route('/verify_students', methods=['GET', 'POST'])
@login_required
def verify_students():
    if request.method == 'POST':
        if current_user.role != 'institution':
            flash('Only institutions can verify students.')
            return redirect(url_for('views.home'))

        student_id = request.form.get('student_id')
        student = Student.query.get(student_id)
        print("called")

        if student and student.institution_id == current_user.id:
            print("calledin")
            student.verified = True
            db.session.commit()
            message = 'Student verification status updated successfully.'
        else:
            message = 'Student not found or unauthorized to verify.'

        return jsonify({'message': message})

    # Get all unverified students for the current institution
    students = Student.query.filter_by(institution_id=current_user.id, verified=False).all()
    return render_template('Applications_management.html', students=students)
    
    
    
@views.route('/teacher_profile', methods=['GET', 'POST'])
@login_required
def teacher_profile():
    
    if current_user.role != 'teacher':
        flash('Not Accessible')
        # print ("calledin")
        return redirect(url_for('views.home'))
    return render_template('Faculty_profile.html')


@views.route('/institute_profile', methods=['GET', 'POST'])
@login_required
def institute_profile():
    
    if current_user.role != 'institution':
        flash('Only institutions can verify students.')
        print ("calledin")
        return redirect(url_for('views.home'))
    
    return render_template('institute_profile.html')

@views.route('/student_profile')
@login_required
def student_profile():
    
    if current_user.role != 'student':
        flash('Not accessible')
        print ("calledin")
        return redirect(url_for('views.home'))
    
    return render_template('student_profile.html')



@views.route('/profile_loader')
@login_required
def profile_loader():
    
    if current_user.role == 'student':
        return redirect(url_for('views.student_profile'))
    elif current_user.role == 'institution':
        return redirect(url_for('views.institute_profile'))
    if current_user.role == 'teacher':
        return redirect(url_for('views.teacher_profile'))
@views.route('/project_feed', methods = ['GET', 'POST'])


@login_required
def project_feed():
    return render_template('project_feed.html')


