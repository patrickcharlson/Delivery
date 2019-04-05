from flask import render_template
from flask_login import login_required

from . import main
from ..models import Customer


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/welcome_page')
@login_required
def welcome_page():
    return render_template('main/welcome_page.html')


@main.route('/customer/<username>')
def customer(username):
    customer = Customer.query.filter_by(username=username).first_or_404()
    return render_template('customer.html', customer=customer)
