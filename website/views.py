# views.py

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .model import Student,Teacher,Institution,Project
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])

def home():
    

    return render_template('student_login.html')



