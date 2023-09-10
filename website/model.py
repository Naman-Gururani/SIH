
from . import db
from flask_login import UserMixin
# from sqlalchemy import Table, ForeignKey, Column, Integer, String, Date
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table, Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
# Base = declarative_base()


    
class Student(db.Model, UserMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Set nullable to False to enforce email presence
    password = db.Column(db.String(150), nullable=False)  # Set nullable to False to enforce password presence
    name = db.Column(db.String(150), nullable=False)  # Set nullable to False to enforce first_name presence
    gender = db.Column(db.String(10), nullable=False)  # Adding gender field (assuming a string field with max length of 10)
    address = db.Column(db.String(200), nullable=True)  # Adding address field (nullable as it might not always be provided)
    country = db.Column(db.String(100), nullable=True)  # Adding country field (nullable as it might not always be provided)
    dob = db.Column(db.String(10), nullable=False)  # Adding dob field (assuming a string field with max length of 10)
    verified = db.Column(db.Boolean, default=False)
    projects = db.relationship('Project', back_populates='student')
    


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    readme_file_path = db.Column(db.String)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', back_populates='projects')

class Institution(db.Model):
    __tablename__ = 'institutions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    teachers = db.relationship('Teacher', back_populates='institution')

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    students = db.relationship('Student', secondary='teacher_student_association', back_populates='teachers')
    institution = db.relationship('Institution', back_populates='teachers')

teacher_student_association = Table(
    'teacher_student_association',
    db.metadata,
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'))
)

