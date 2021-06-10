from flask import Flask, jsonify, request, url_for, jsonify, session, render_template, make_response, redirect, render_template, abort
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,PasswordField
from wtforms.validators import DataRequired,Email,EqualTo,Length,NoneOf,InputRequired
from wtforms.fields.html5 import DateField
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user


app = Flask(__name__)
app.config['DEBUG'] = True

#create secret key for CSRF protection 

app.config['SECRET_KEY'] = "hI9t6Bt4Dl1!8F"

#add database 

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:F41r4cr3/P1pps@localhost/themindgarden'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False


#instantiate database 

db = SQLAlchemy(app)

#initialise migrate 
migrate = Migrate(app, db)



# create users table 

class Users(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True,default=uuid4)
    first_name= db.Column(db.String(100), nullable=False)
    last_name= db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email_address = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    date_created=db.Column(db.DateTime,nullable=False, default= datetime.utcnow)
    last_seen= db.Column(db.DateTime,nullable=True)
    admin = db.Column(db.Boolean,unique=False,nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    
    @password.setter

    # hash password
    def password(self, password):
        self.password_hash= generate_password_hash(password)

    '''verify password by checking hashed password and password given by user''' 
    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)
        
    # def is_active(self):
    #     """True, as all users are active."""
    #     return True

    # def get_id(self):
    #     """Return the email address to satisfy Flask-Login's requirements."""
    #     return self.email_address

    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated

    # def is_anonymous(self):
    #     """False, as anonymous users aren't supported."""
    #     return False

    def __repr__(self):
        return '<User {}>'.format(self.id)


# db.create_all()

login_manager= LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


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


# Create route 
@app.route('/' , methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/createaccount',  methods=['GET',"POST"])
def createaccount():
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    first_name= None
    last_name= None
    birthdate= None
    email_address=None
    password=None
    confirm= None
    accept_tos= None
    ''' create form instance to pass through to html'''
    form= CreateAccountForm()
    '''validate form to check that each feild has been completed correctly''' 
    if form.validate_on_submit():
        '''check that email address doesn't already exist'''
        user= Users.query.filter_by(email_address=form.email_address.data).first()
        ''' if user doesnt already exist, add to db'''
        if user is None:
            first_name= form.first_name.data
            form.first_name.data= " "
            last_name= form.last_name.data
            form.last_name.data= " "
            birthdate= form.birthdate.data.strftime('%d-%m-%Y')
            form.birthdate.data = datetime.strptime("01-01-2020", '%d-%m-%Y')
            email_address= form.email_address.data
            form.email_address.data= " "
            password= form.password_hash.data
            form.password_hash.data= " "
            hashed_password= generate_password_hash(password)
            user= Users(first_name= first_name, last_name= last_name, dob= birthdate,email_address=email_address,password_hash= hashed_password)
            print(user)
            db.session.add(user)
            db.session.commit()
        else:
            ''' if user does exist, display message'''
            message= "An account with that email address already exists"
            return render_template("createaccount.html", first_name=first_name,last_name=last_name,birthdate=birthdate,
    email_address=email_address, password=password, confirm=confirm, accept_tos= accept_tos, form= form,message=message)
    return render_template("createaccount.html", first_name=first_name,last_name=last_name,birthdate=birthdate,
    email_address=email_address, password=password, confirm=confirm, accept_tos= accept_tos, form= form)
    

@app.route('/login', methods= ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    email_address= None
    password_hash=None
    user=None
    form= LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email_address=form.email_address.data).first()
        if user is not None and user.verify_password(form.password_hash.data):
            login_user(user ,'''form.remember_me.data''')
            home = url_for('index')
            return redirect(home)
        else:
            message= "You have entered an incorrect email address or password"
            return render_template("login.html", email_address=email_address, password_hash=password_hash,form=form,message=message)
    return render_template("login.html", email_address=email_address, password_hash=password_hash,form=form)

@app.route('/forgottenpassword', methods=["GET", "POST"])
def forgottenpassword():
    email_address= None
    form= ForgottenPasswordForm()
    if form.validate_on_submit():
        email_address=form.email_address.data
        form.email_address.data= " "
    return render_template("forgottenpassword.html", email_address=email_address, form=form)

@app.route('/yourgarden')
@login_required
def yourgarden():
    return render_template("yourgarden.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("logout.html")


if __name__ == '__main__':
    app.run(port=80, debug=True)

    