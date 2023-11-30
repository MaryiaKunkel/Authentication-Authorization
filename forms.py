# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, RadioField, SelectField, URLField, IntegerRangeField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Optional, NumberRange, Email, Length

class RegisterForm(FlaskForm):
    '''Add a new user'''
    username=StringField('User Name', validators=[InputRequired(message='Username is required'), Length(max=20)])
    password=PasswordField('Password', validators=[InputRequired(message='Password is required')])
    email=EmailField('Email', validators=[InputRequired(message='Email is required'), Email(), Length(max=50)])
    first_name=StringField('First name', validators=[InputRequired(message='First name is required'), Length(max=30)])
    last_name=StringField('Last name', validators=[InputRequired(message='Last name is required'), Length(max=30)])

class LoginForm(FlaskForm):
    username=StringField('User Name', validators=[InputRequired(message='Username is required'), Length(max=20)])
    password=PasswordField('Password', validators=[InputRequired(message='Password is required')])

class FeedbackForm(FlaskForm):
    title=StringField('Title', validators=[InputRequired(message='Title is required'), Length(max=100)])
    content=TextAreaField('Content', validators=[InputRequired(message='Text is required')])