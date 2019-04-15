from flask import flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .forms import RegistrationForm, LoginForm, RequestResetPasswordForm, PasswordResetForm
from ..email import send_email
from ..models import Customer, db


@auth.route('/register', methods=['GET', 'POST'])
def register():
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
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer is not None and customer.verify_password(form.password.data):
            login_user(customer, form.remember_me.data)
            flash("You are now logged in", 'form-success')
            return redirect(url_for('main.welcome_page'))
        else:
            flash('Invalid username or password', 'form-error')
    return render_template('auth/login.html', form=form, title='Login')


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
        return redirect(url_for('main.welcome_page'))
    if current_user.confirm(token):
        flash('You have confirmed your account', 'form-success')
    else:
        flash('The confirmation link is invalid or has expired ', 'form-error')
    return redirect(url_for('main.index'))


# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping()
#         if not current_user.confirmed \
#                 and request.endpoint[:5] != 'auth.':
#             return redirect(url_for('auth.unconfirmed'))
#
#
# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')
#
#
# @auth.route('/confirm')
# @login_required
# def resend_confirmation():
#     token = current_user.generate_confirmation_token()
#     send_email(current_user.email, 'Confirm Your Account',
#                'auth/email/confirm', customer=current_user, token=token)
#     flash('A new confirmation email has been sent to {}'.format(current_user.email),
#           'form-info')
#     return redirect(url_for('main.welcome_page'))
