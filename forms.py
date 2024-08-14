from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email

#ADD EMAIL VALIDATOR

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name',validators=[InputRequired(), Length(max=30)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    email = StringField('Email',validators=[InputRequired(), Length( max=50), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=55 )])
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=55)])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = TextAreaField('Feedback', validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete Form"""
