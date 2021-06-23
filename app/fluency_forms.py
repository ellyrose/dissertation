from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,PasswordField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired,Email,EqualTo,Length,NoneOf,InputRequired, ValidationError
from wtforms.fields.html5 import DateField

DAYS= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DATE=range(1,32)
MONTH= ["January","February","March","April","May","June","July","August","September","October","November","December"]
YEAR= range(1950,2051)
SEASON= ["Spring","Summer", "Automn","Winter"]

class Fluency_1(FlaskForm):
    day= SelectField(label="What day is it?", validators=[DataRequired()], choices=DAYS)
    date= SelectField(label="What is the date?", validators=[DataRequired()], choices=DATE)
    month= SelectField(label="What month are we in?", validators=[DataRequired()], choices=MONTH)
    year= SelectField(label="What year is it?", validators=[DataRequired()], choices=YEAR)
    season= SelectField(label="What season are we in?", validators=[DataRequired()], choices=SEASON)
    
    submit= SubmitField("Submit")


