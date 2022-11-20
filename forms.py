from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class RegisterUser(FlaskForm):
    """Form for registering user"""

    first_name = StringField("First Name",
                            validators=[InputRequired()])
    last_name = StringField("Last Name",
                            validators=[InputRequired()])
    email = StringField("Email",
                            validators=[InputRequired()])
    username = StringField("Username",
                            validators=[InputRequired()])
    password = PasswordField("Password",
                            validators=[InputRequired()])

class LoginUser(FlaskForm):
    """Form for logging in users"""
    username = StringField("Username",
                            validators=[InputRequired()])
    password = PasswordField("Password",
                            validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form for Feedback"""
    title = StringField("Title",
                            validators=[InputRequired()])
    content = StringField("Content",
                            validators=[InputRequired()])
