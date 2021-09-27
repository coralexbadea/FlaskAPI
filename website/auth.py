from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import Role

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.get_json()
        email = login["email"]
        password = login["password"]
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return "success"
            else:
                return "bad password"
        else:
            return "dont exists"
    return "get_login"


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "logout success"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        sign_up = request.get_json()
        email = sign_up["email"]
        first_name = sign_up["firstName"]
        password1 = sign_up["password1"]
        password2 = sign_up["password2"]

        user = User.query.filter_by(email=email).first()
        if user:
            return "user_exists"
        elif len(email) < 4:
            return "short email"
        elif len(first_name) < 2:
            return "first name"
        elif password1 != password2:
            return "pass match"
        elif len(password1) < 3:
            return "pass short"
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            role = Role.query.filter_by(role_name="ADMIN").first()
            new_user.roles.append(role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return "success"

    return "get_sign-up"
