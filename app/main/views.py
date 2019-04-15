from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from . import main
from .forms import ChangePasswordForm, ChangeEmailForm, EditProfileForm
from .. import db
from ..email import send_email
from ..models import Customer


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/welcome_page')
@login_required
def welcome_page():
    return render_template('main/welcome_page.html')


@main.route('/customer/<first_name>')
def customer(first_name):
    customer = Customer.query.filter_by(first_name=first_name).first_or_404()
    return render_template('customer.html', customer=customer)


@main.route('/customer/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("your password has been updated!", 'form-success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid password', 'form-error')
    return render_template('main/change_password.html', form=form)


@main.route('/customer/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_change_email_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       customer=current_user, token=token)
            flash('A confirmation link has been sent to {}'.format(new_email),
                  'form-info')
            return redirect(url_for('auth.login'))
        flash('Invalid email address', 'form-error')
    return render_template('main/change_email.html', form=form)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        current_user.news_letter = form.news_letter.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your Profile has been updated', 'form-success')
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.phone_number.data = current_user.phone_number
    form.news_letter.data = current_user.news_letter
    return render_template('main/edit-profile.html', form=form)
