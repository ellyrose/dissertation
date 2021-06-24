from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,IntegerField
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

class Fluency_2(FlaskForm):

    submit= SubmitField("Submit")

class Fluency_3(FlaskForm):
    v1= IntegerField(label="Answer 1", validators=[DataRequired()])
    v2= IntegerField(label="Answer 2", validators=[DataRequired()])
    v3= IntegerField(label="Answer 3", validators=[DataRequired()])
    v4= IntegerField(label="Answer 4", validators=[DataRequired()])
    v5= IntegerField(label="Answer 5", validators=[DataRequired()])

    submit= SubmitField("Submit")

class Fluency_4(FlaskForm):

    submit= SubmitField("Submit")

class Fluency_5(FlaskForm):
    v1= StringField(label="What is the name of the current Prime Minister?", validators=[DataRequired()])
    v2= StringField(label="Name the first woman who was Prime Minister:", validators=[DataRequired()])
    v3= StringField(label="Name the USA President:", validators=[DataRequired()])
    v4= StringField(label="What is the name of the USA President who was assassinated in the 1960s?", validators=[DataRequired()])
   
    submit= SubmitField("Submit")

class Fluency_6(FlaskForm):

    submit= SubmitField("Submit")


class Fluency_7(FlaskForm):
    v1= StringField(label="Name of item 1:", validators=[DataRequired()])
    v2= StringField(label="Name of item 2:", validators=[DataRequired()])
    v3= StringField(label="Name of item 3:", validators=[DataRequired()])
    v4= StringField(label="Name of item 4:", validators=[DataRequired()])
    v5= StringField(label="Name of item 5:", validators=[DataRequired()])
    v6= StringField(label="Name of item 6:", validators=[DataRequired()])
    v7= StringField(label="Name of item 7:", validators=[DataRequired()])
    v8= StringField(label="Name of item 8:", validators=[DataRequired()])
    v9= StringField(label="Name of item 9:", validators=[DataRequired()])
    v10= StringField(label="Name of item 10:", validators=[DataRequired()])
    v11= StringField(label="Name of item 11:", validators=[DataRequired()])
    v12= StringField(label="Name of item 12:", validators=[DataRequired()])

    submit= SubmitField("Submit")