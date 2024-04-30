from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo



class registerUser(FlaskForm):
 username = StringField('Username',validators =[DataRequired(), Length (min = 6, max = 15)], render_kw ={"placeholder":"Example: student1"})
 password = PasswordField('New password', validators = [DataRequired(), Length (min=4, max =10), EqualTo('confirm',message='password does not match')])
 confirm = PasswordField ('Confirm password', validators = [DataRequired(), EqualTo('confirm',message='password does not match')])
 role = SelectField(
        'Role',
        validators=[DataRequired()],
        choices=[
            ('admin', 'Admin'),
            ('librarian', 'Librarian'),
            ('faculty', 'Faculty'),
            ('student', 'Student'),
            ('public', 'Public')
        ]
    )
 submit = SubmitField ("Register")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')