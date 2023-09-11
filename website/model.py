
from . import db
from flask_login import UserMixin
# from sqlalchemy import Table, ForeignKey, Column, Integer, String, Date
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table, Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
# Base = declarative_base()


class Teacher(db.Model, UserMixin):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    institution = db.relationship('Institution', back_populates='teachers')
    role = db.Column(db.String(20), nullable=False, default='teacher')  

class Student(db.Model, UserMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.String(10), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    projects = db.relationship('Project', back_populates='student')
    role = db.Column(db.String(20), nullable=False, default='student')
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))  # New field
    institution = db.relationship('Institution', backref='students')  # New relationship
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))  # New field
    teachers = db.relationship('Teacher', backref='students')  # New relationship
    db.relationship('Institution', secondary='institution_student_association', back_populates='students')


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    readme_file_path = db.Column(db.String)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', back_populates='projects')



class Institution(db.Model,UserMixin):
    __tablename__ = 'institutions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    teachers = db.relationship('Teacher', back_populates='institution')
    role = db.Column(db.String(20), nullable=False, default='institution')
