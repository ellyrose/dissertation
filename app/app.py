from flask import Flask, jsonify, request, url_for, jsonify, redirect, session, render_template, make_response, redirect, render_template, abort
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,PasswordField,HiddenField
from wtforms.validators import DataRequired,email_validator,Email,EqualTo,Length,NoneOf,InputRequired
from wtforms.fields.html5 import DateField
import datetime
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "hI9t6Bt4Dl1!8F"

# Create form classes to be used on html files 

class CreateAccountForm(FlaskForm):
    first_name= StringField("First Name", validators=[DataRequired(),Length(min= 1, max=30, 
    message="Value entered exceeds maximum length")], description="First name")

    last_name= StringField("Last Name", validators=[DataRequired(),Length(min= 1, max=30, 
    message="Value entered exceeds maximum length")], description="Last name")

    birthdate= DateField("Birthdate", validators=[DataRequired()])

    email_address= StringField("Email address", validators=[DataRequired(),Email(message="Your email address is not valid.")])

    password = PasswordField('Password', validators=[InputRequired(),
    Length(min=12, max=30, message="Your password must contain at least 12 characters"),
       EqualTo('confirm', message='The two passwords must match')])
    

    confirm = PasswordField('Repeat Password', validators=[DataRequired()])

    accept_tos = BooleanField('I accept the Terms and Conditions', [validators.DataRequired()])

    submit= SubmitField("Submit")




# Create route 
@app.route('/home' , methods=['GET'])
def index():
    name= "Elly"
    return render_template("index.html")

@app.route('/createaccount',  methods=['GET',"POST"])
def createaccount():
    first_name= None
    last_name= None
    birthdate= None
    email_address=None
    password=None
    confirm= None
    accept_tos= None
    form= CreateAccountForm()
    # validate form 
    if form.validate_on_submit():
        first_name= form.first_name.data
        form.first_name.data= " "
        last_name= form.last_name.data
        form.last_name.data= " "
        birthdate= form.birthdate.data.strftime('%d-%m-%Y')
        form.birthdate.data = datetime.strptime("01-01-2020", '%d-%m-%Y')
        email_address= form.email_address.data
        form.email_address.data= " "
        password= form.password.data
        form.password.data= " "
    return render_template("createaccount.html", first_name=first_name,last_name=last_name,birthdate=birthdate,
    email_address=email_address, password=password, confirm=confirm, accept_tos= accept_tos, form= form)
    

@app.route('/createaccount',  methods=['POST'])
def post_createaccount():
    return render_template("createaccount.html")

    

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/forgottenpassword')
def forgottenpassword():
    return render_template("forgottenpassword.html")

@app.route('/yourgarden')
def yourgarden():
    name="Elly"
    return render_template("yourgarden.html")

@app.route('/logout')
def logout():
    return render_template("logout.html")


if __name__ == '__main__':
    app.run(port=80, debug=True)

    