from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,PasswordField
from wtforms.validators import DataRequired,Email,EqualTo,Length,NoneOf,InputRequired
from wtforms.fields.html5 import DateField

# Create form classes to be used on html files 

class CreateAccountForm(FlaskForm):
    first_name= StringField("First Name", validators=[DataRequired(),Length(min= 1, max=30, 
    message="Value entered exceeds maximum length")], description="First name")

    last_name= StringField("Last Name", validators=[DataRequired(),Length(min= 1, max=30, 
    message="Value entered exceeds maximum length")], description="Last name")

    birthdate= DateField("Birthdate", validators=[DataRequired()])

    email_address= StringField("Email address", validators=[DataRequired(),Email(message="Your email address is not valid.")])

    password_hash = PasswordField('Password', validators=[InputRequired(),
    Length(min=12, max=30, message="Your password must contain at least 12 characters"),
       EqualTo('confirm', message='The two passwords must match')])
    

    confirm = PasswordField('Repeat Password', validators=[DataRequired()])

    accept_tos = BooleanField('I accept the Terms and Conditions', [validators.DataRequired()])

    submit= SubmitField("Submit")


class LoginForm(FlaskForm):
    email_address= StringField("Email address", validators=[DataRequired(),Email(message="Your email address is not valid.")])

    password_hash = PasswordField('Password', validators=[DataRequired()])

    submit= SubmitField("Submit")

class ForgottenPasswordForm(FlaskForm):
    email_address= StringField("Email address", validators=[DataRequired(),Email(message="Your email address is not valid.")])
   
    submit= SubmitField("Submit")

class ResetPasswordForm(FlaskForm):
    password_hash = PasswordField('Password', validators=[InputRequired(),
    Length(min=12, max=30, message="Your password must contain at least 12 characters"),
       EqualTo('confirm', message='The two passwords must match')])
    

    confirm = PasswordField('Repeat Password', validators=[DataRequired()])

    submit= SubmitField("Submit")
