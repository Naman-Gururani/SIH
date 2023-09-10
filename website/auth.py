# #auth.py
# from flask import Blueprint, render_template, request, flash, redirect, url_for
# from .model import Student,Teacher,Institution,Project
# from werkzeug.security import generate_password_hash, check_password_hash
# from . import auth,db   ##means from __init__.py import db
# from flask_login import login_user, login_required, logout_user, current_user

# auth = Blueprint('auth', __name__)


# app=Flask(__name__)
# @app.route('/',methods=['GET','POST'])
# def home():
#     if request.method=='POST':
#         # Handle POST Request here
#         return render_template('index.html')
#     return render_template('index.html')

# if __name__ == '__main__':
#     #DEBUG is SET to TRUE. CHANGE FOR PROD
#     app.run(port=5000,debug=True)