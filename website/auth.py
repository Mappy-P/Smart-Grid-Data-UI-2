from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# @auth.route('/login', methods=['GET', 'POST'])   
# def login():
#     data = request.form
#     print(data)
#     return render_template("login.html")

# @auth.route('/logout')  
# def logout():
#     return redirect(url_for('auth.login'))

# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         firstName = request.form.get('first-name')
#         password = request.form.get('password')
#         password1 = request.form.get('password1')

#         if password != password1:
#             flash("Passwords don't match", category='error')
#         else:
#             new_user = User(email=email, first_name=firstName, password=generate_password_hash(password, method = 'sha256'))
#             db.session.add(new_user)
#             db.session.commit()
#             flash("Your account has succesfully been created!", category='succes')
#             return redirect(url_for('views.home'))

#     return render_template("sign_up.html")
