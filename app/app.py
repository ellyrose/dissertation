from hashlib import new
from flask import Flask, flash, jsonify, request, url_for, jsonify, session, render_template, make_response, redirect, render_template, abort
from datetime import datetime
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
import os
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from forms import LoginForm,CreateAccountForm,ResetPasswordForm,ForgottenPasswordForm, EditDetailsForm,LoggedInResetPasswordForm,AdminEditForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



app = Flask(__name__)


#create secret key for CSRF protection, session etc 

app.config['SECRET_KEY'] = "hI9t6Bt4Dl1!8F"

#set session time so a user is logged out after 1 hour of inactivity 
app.config['PERMANENT_SESSION_LIFETIME']= timedelta(minutes=60)



#add database 

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:F41r4cr3/P1pps@localhost/themindgarden'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

#congifure email sending 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')


#configure app mail sending 

app.config['MAIL_SUBJECT_PREFIX'] = 'The Mind Garden |'
app.config['MAIL_SENDER'] = 'The Mind Garden <themindgarden21@gmail.com>'

#initialize mail

mail = Mail(app)

# function to send emails 

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

#instantiate database 

db = SQLAlchemy(app)

#initialise migrate 
migrate = Migrate(app, db)

#Use limiter to prevent brute force attacks for a given IP address 

limiter = Limiter(
    app,
    key_func=get_remote_address,
)

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

    ''' functions to generate tokens used in reset password'''
    '''Expiration set to one hour'''
        
    def generate_reset_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        '''the token is made and the user-id for the user of given email is sent'''
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return Users.query.get(id)
           


    def __repr__(self):
        return '<User {}>'.format(self.id)


# db.create_all()

login_manager= LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

'''ROUTES'''

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
@limiter.limit(["100 per day","50 per hour"])
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
            login_user(user ,remember=False)
            home = url_for('index')
            session.permanent = True
            return redirect(home)
        else:
            message= "You have entered an incorrect email address or password"
            return render_template("login.html", email_address=email_address, password_hash=password_hash,form=form,message=message)
    return render_template("login.html", email_address=email_address, password_hash=password_hash,form=form)


@app.route('/forgottenpassword', methods=["GET", "POST"])
def forgottenpassword():
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    email_address= None
    form= ForgottenPasswordForm()
    if form.validate_on_submit():
        email_address=form.email_address.data.lower()
        form.email_address.data= " "
        user= Users.query.filter_by(email_address=email_address).first()
        if user is None:
            email_address= True
            return render_template("forgottenpassword.html", email_address=email_address, form=form)
        token = user.generate_reset_token()
        send_email(user.email_address,'Reset Your Password',
                   '/mail/password_reset', user=user, token=token)
    return render_template("forgottenpassword.html", email_address=email_address, form=form)


@app.route('/resetpassword/<token>', methods=["GET", "POST"])
def resetpassword(token):
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    user= Users.verify_reset_token(token)
    form= ResetPasswordForm()
    if user is None:
        return render_template("resetpassword.html", form=form, error=True)
    if form.validate_on_submit():
        password_hash= form.password_hash.data
        form.password_hash.data= " "
        form.confirm.data= " "
        hashed_password= generate_password_hash(password_hash)
        user.password_hash= hashed_password
        db.session.commit()
        return render_template("success.html")
    return render_template("resetpassword.html", form=form, error=False)

@app.route('/resetpassword', methods=["GET", "POST"])
@login_required
def loggedinresetpassword():
    user= current_user
    new_password=None
    confirm= None
    current_password= None
    message=None
    form= LoggedInResetPasswordForm()
    if form.validate_on_submit():
        current_password= form.password_hash.data
        new_password= form.new_password.data
        form.new_password.data= " "
        form.password_hash.data= " "
        form.confirm.data= " "
        if user.verify_password(current_password):
            new_password_hash=generate_password_hash(new_password)
            user.password_hash= new_password_hash
            try:
                db.session.commit()
                message= "Your details have been updated!"
                return render_template("resetpassword.html", message=message,form=form, user=user, 
                password_hash= current_password, new_password= new_password, confirm=confirm)   
            except:
                 message= "Sorry there was an error, please try again."
                 return render_template("resetpassword.html", message=message,form=form, user=user, 
                 password_hash= current_password, new_password= new_password, confirm=confirm)
        else:
            message ="Sorry, your current password was incorrect"
            return render_template("resetpassword.html", message=message,form=form, user=user, 
                 password_hash= current_password, new_password= new_password, confirm=confirm)
    return render_template("resetpassword.html", form=form, user=user, 
                 password_hash= current_password, new_password= new_password, confirm=confirm)

   
@app.route('/yourgarden')
@login_required
def yourgarden():
    return render_template("yourgarden.html")


@app.route('/account',methods=["GET", "POST"])
@login_required
def account():
    user= current_user
    first_name= user.first_name
    last_name = user.last_name
    birthdate= user.dob
    email_address= user.email_address
    current_password=None
    message= None
    form= EditDetailsForm()
    if form.validate_on_submit():
        first_name= form.first_name.data
        last_name= form.last_name.data
        birthdate= form.birthdate.data
        email_address=form.email_address.data.lower()
        current_password= form.password_hash.data
        if user.verify_password(current_password):
            user.first_name= first_name
            user.last_name= last_name
            user.dob= birthdate
            user.email_address= email_address
            try:
                db.session.commit()
                form.first_name.data= user.first_name
                form.last_name.data = user.last_name
                form.birthdate.data= user.dob
                form.email_address.data= user.email_address
                message= "Your details have been updated!"
                return render_template("account.html", message=message,form=form, user=user, 
                first_name= first_name, last_name= last_name, dob= birthdate,email_address=email_address,
                password_hash= current_password)   
            except:
                form.first_name.data= user.first_name
                form.last_name.data = user.last_name
                form.birthdate.data= user.dob
                form.email_address.data= user.email_address
                message= "Sorry there was an error, please try again."
                return render_template("account.html", message=message,form=form, user=user, 
                first_name= first_name, last_name= last_name, dob= birthdate,email_address=email_address,
                password_hash= current_password)   
        else:
            message= "You entered an incorrect password."
    return render_template("account.html", message=message,form=form, user=user, first_name= first_name, 
    last_name= last_name, dob= birthdate,email_address=email_address,password_hash= current_password)   

@app.route('/logout')
@login_required
def logout():
    user= current_user
    user.last_seen= datetime.utcnow()
    db.session.commit()
    logout_user()
    return render_template("logout.html")


''' Admin panel page '''
@app.route('/admin')
@login_required
def admin():
    user= current_user
    if not user.admin:
        return page_not_found(404)
    all_users= Users.query.order_by(Users.date_created)
    return render_template("admin.html", all_users=all_users)

''' Admin update user details page '''
@app.route('/update/<id>',methods=["GET", "POST"])
@login_required
def update(id):
    user= current_user
    if not user.admin:
        return page_not_found(404)
    update_user= Users.query.get_or_404(id)
    first_name= update_user.first_name
    last_name = update_user.last_name
    birthdate= update_user.dob
    email_address= update_user.email_address
    message= None
    form= AdminEditForm()
    if form.validate_on_submit():
        first_name= form.first_name.data
        last_name= form.last_name.data
        birthdate= form.birthdate.data
        email_address=form.email_address.data.lower()
        update_user.first_name= first_name
        update_user.last_name= last_name
        update_user.dob= birthdate
        update_user.email_address= email_address
        try:
            db.session.commit()
            form.first_name.data= update_user.first_name
            form.last_name.data = update_user.last_name
            form.birthdate.data= update_user.dob
            form.email_address.data= update_user.email_address
            message= "User's details have been updated!"
            return render_template("update_user.html", form=form, update_user=update_user,first_name=first_name, last_name=last_name,
            birthdate=birthdate, email_address=email_address, message=message)
        except:
            form.first_name.data= update_user.first_name
            form.last_name.data = update_user.last_name
            form.birthdate.data= update_user.dob
            form.email_address.data= update_user.email_address
            message= "Sorry there was an error, please try again."
            return render_template("update_user.html", form=form,update_user=update_user,first_name=first_name, last_name=last_name,
            birthdate=birthdate, email_address=email_address, message=message)
    return render_template("update_user.html", form=form, update_user=update_user,first_name=first_name, last_name=last_name,
    birthdate=birthdate, email_address=email_address)

@app.route('/delete/<id>')
@login_required
def delete(id):
    user= current_user
    if not user.admin:
        return page_not_found(404)
    update_user= Users.query.get_or_404(id)
    first_name= update_user.first_name
    last_name = update_user.last_name
    birthdate= update_user.dob
    email_address= update_user.email_address
    message= None
    form= AdminEditForm()
    try:
        db.session.delete(update_user)
        db.session.commit()
        all_users=  Users.query.order_by(Users.date_created)
        flash("User has been deleted!")
        return render_template("admin.html", all_users=all_users)
    except:
        flash("There was a problem, please try again.")
        return render_template("admin.html", all_users=all_users)



if __name__ == '__main__':
    app.run(port=80, debug=True)
   

    