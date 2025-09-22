from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import main_bp

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')
