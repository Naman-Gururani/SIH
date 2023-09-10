
from . import db
from flask_login import UserMixin
from sqlalchemy import Table, ForeignKey, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy


Base = declarative_base()
db = SQLAlchemy()

    
class Student(Base, UserMixin):
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
    projects = relationship('Project', back_populates='student')
    

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    project_name = Column(String)
    readme_file_path = Column(String)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship('Student', back_populates='projects')

class Institution(Base):
    __tablename__ = 'institutions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    teachers = relationship('Teacher', back_populates='institution')

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    institution_id = Column(Integer, ForeignKey('institutions.id'))
    students = relationship('Student', secondary='teacher_student_association', back_populates='teachers')
    institution = relationship('Institution', back_populates='teachers')

teacher_student_association = Table(
    'teacher_student_association',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.id')),
    Column('student_id', Integer, ForeignKey('students.id'))
)
