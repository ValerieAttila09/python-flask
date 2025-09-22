from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from . import auth_bp
from ..models import User
from .forms import LoginForm, RegistrationForm

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user is not None:
            return 'Username already exists'
        user = User(username=form.username.data, password=form.password.data)
        user.save()
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user is None or not user.check_password(form.password.data):
            return '<h1>Invalid username or password</h1>'
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))
