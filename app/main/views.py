from flask import render_template
from flask_login import login_required

from . import main


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/welcome_page')
@login_required
def welcome_page():
    return render_template('main/welcome_page.html')
