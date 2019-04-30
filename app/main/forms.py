from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length

from ..models import Customer


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


class EditProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[Length(0, 64)])
    last_name = StringField('Last name', validators=[Length(0, 64)])
    email = StringField('Email', render_kw={'disabled': ''})
    phone_number = StringField('Mobile')
    news_letter = BooleanField('Subscribe to NewsLetter')
    submit = SubmitField('SAVE CHANGES')


class TownForm(FlaskForm):
    towns = [('Nrb', 'Nairobi'), ('Eld', 'Eldoret'), ('ksm', 'Kisumu City'), ('naks', 'Nakuru'), ('msa', 'Mombasa')]
    myCity = SelectField('Select your City', choices=towns,
                         validators=[DataRequired()], render_kw={'placeholder': 'Select Your City'})
