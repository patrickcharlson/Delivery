from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from ..models import Customer


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(1, 64)])
    first_name = StringField('First name:', validators=[DataRequired()])
    last_name = StringField('Last name:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[
        DataRequired(), EqualTo('password2', message='passwords must match')])
    password2 = PasswordField('Confirm Password:', validators=[DataRequired()])
    submit = SubmitField('Sign up Now')

    def validate_email(self, field):
        if Customer.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if Customer.query.filter_by(username=field.data).first():
            raise ValidationError("username already in use!")


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if Customer.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address!')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new Password', validators=[DataRequired()])
    submit = SubmitField('Update password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if Customer.query.filter_by(email=field.data).first():
            raise ValidationError("Email already in use!")


class SubscribeForm(FlaskForm):
    cities = [('choose', 'Select your City'), ('nrb', 'Nairobi'), ('eld', 'Eldoret'), ('ksm', 'Kisumu City'),
              ('msa', 'Mombasa'), ('naks', 'Nakuru')]
    City = SelectField(choices=cities, validators=[DataRequired()])
    email = StringField(render_kw={'placeholder': 'E-mail'}, validators=[DataRequired()])
    submit = SubmitField('Subscribe newsletter')
    boolean = BooleanField('I have read and accepted the Terms and conditions and the Privacy policy')
