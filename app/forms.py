from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class registerUser(FlaskForm):
 username = StringField('Username',validators =[DataRequired(), Length (min = 4, max = 15)], render_kw ={"placeholder":"Example: student1"})
 password = PasswordField('New password', validators = [DataRequired(), Length (min=4, max =10), EqualTo('confirm',message='password does not match')])
 confirm = PasswordField ('Confirm password', validators = [DataRequired(), EqualTo('confirm',message='password does not match')])
 role = SelectField(
        'Role',
        validators=[DataRequired()],
        choices=[
            ('Admin', 'Admin'),
            ('Librarian', 'Librarian'),
            ('Faculty', 'Faculty'),
            ('Student', 'Student'),
            ('Public', 'Public')
        ]
    )
 submit = SubmitField ("Register")

class loginUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class deleteUser(FlaskForm): #maybe this class is not needed later 
    submit = SubmitField('Delete')