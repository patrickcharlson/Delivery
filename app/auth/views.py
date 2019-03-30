from flask import flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm
from ..models import Customer, db


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # noinspection PyArgumentList
        customer = Customer(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)
        db.session.add(customer)
        db.session.commit()
        flash("You can now login")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer is not None and customer.verify_password(form.password.data):
            login_user(customer, form.remember_me.data)
            return redirect(url_for('main.welcome_page'))
        else:
            flash('invalid username or password')
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('main.index'))
