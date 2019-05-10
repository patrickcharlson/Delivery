from flask import flash, redirect, url_for, render_template, request
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .forms import RegistrationForm, LoginForm, RequestResetPasswordForm, PasswordResetForm, SubscribeForm
from ..email import send_email
from ..models import Customer, db


@auth.route('/register', methods=['GET', 'POST'])
def register():
    s_form = SubscribeForm()
    form = RegistrationForm()
    if form.validate_on_submit():
        # noinspection PyArgumentList
        customer = Customer(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data)
        db.session.add(customer)
        db.session.commit()
        token = customer.generate_confirmation_token()
        send_email(customer.email, 'Confirm your Account',
                   'auth/email/confirm', customer=customer, token=token)
        flash("A confirmation email has been sent to {}".format(customer.email),
              'form-info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title='Sign Up', s_form=s_form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    s_form = SubscribeForm()
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer is not None and customer.verify_password(form.password.data):
            login_user(customer)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('pizzeria.products')
            flash("You are now logged in", 'form-success')
            return redirect(next)
        flash('Invalid username or password', 'form-error')
    return render_template('auth/login.html', form=form, title='Login', s_form=s_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'form-info')
    return redirect(url_for('main.index'))


@auth.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer:
            token = customer.generate_reset_token()
            send_email(customer.email, 'Reset your Password',
                       'auth/email/reset_password',
                       customer=customer, token=token)
            flash('A password reset link has been sent to {}'.format(
                form.email.data), 'form-info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, title='Password Reset')


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer is None:
            flash('Invalid email address!', 'form-error')
            return redirect(url_for('main.index'))
        if customer.password_reset(token, form.password.data):
            flash('Your password has been updated!', 'form-success')
            return redirect(url_for('auth.login'))
        else:
            flash('The password link is invalid or has expired', 'form-error')
    return render_template('auth/email/reset_password.html', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash("Email address has been updated!", 'form-success')
    else:
        flash("Invalid request", 'form-warning')
    return redirect(url_for('auth.login'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('pizzeria.products'))
    if current_user.confirm(token):
        flash('You have confirmed your account', 'form-success')
    else:
        flash('The confirmation link is invalid or has expired ', 'form-error')
    return redirect(url_for('main.index'))
