from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

bootstrap = Bootstrap(app)


class DataForm(FlaskForm):
    username = StringField('Enter your name', validators=[DataRequired, Length(min=4, max=25)])
    email = StringField('Email Address', validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired, EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    Submit = SubmitField('Login')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DataForm()

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
