from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


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
