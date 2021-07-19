from flask import Flask, flash, request, url_for, jsonify, session, render_template, make_response, redirect, render_template, abort
from datetime import datetime, timedelta, date as dt
from flask_admin.base import AdminIndexView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_migrate import Migrate, current
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
import os
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from forms import *
from fluency_forms import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import calendar
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink





app = Flask(__name__)


#create secret key for CSRF protection, session etc 

app.config['SECRET_KEY'] = "hI9t6Bt4Dl1!8F"

#set session time so a user is logged out after 1 hour of inactivity 
app.config['PERMANENT_SESSION_LIFETIME']= timedelta(minutes=60)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'



#add database 

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:F41r4cr3/P1pps@localhost/themindgarden'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

#instantiate database 

db = SQLAlchemy(app)


#congifure email sending 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')




#initialize mail

mail = Mail(app)


#configure app mail sending 

app.config['MAIL_SUBJECT_PREFIX'] = 'The Mind Garden |'
app.config['MAIL_SENDER'] = 'The Mind Garden <themindgarden21@gmail.com>'

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)



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

    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    first_name= db.Column(db.String(100), nullable=False)
    last_name= db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email_address = db.Column(db.String(120), nullable=False, unique=True)
    country = db.Column(db.String(200), nullable=False, unique=False)
    password_hash = db.Column(db.String, nullable=False)
    date_created=db.Column(db.DateTime,nullable=False, default= datetime.utcnow)
    last_seen= db.Column(db.DateTime,nullable=True)
    admin = db.Column(db.Boolean,unique=False,nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash= generate_password_hash(password)

    '''verify password by checking hashed password and password given by user''' 
    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    ''' functions to generate tokens used in reset password'''
    '''Expiration set to one hour'''
        
    def generate_reset_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        '''the user ID is encoded using the secret key, and the token expiration set to 1 hour'''
        self.id = str(self.id)
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

class Test(db.Model):
    __tablename__ = "test"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    userid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    date_completed= db.Column(db.DateTime,nullable=True)
    module_1_score= db.Column(db.Integer, default= 0)
    module_1_status = db.Column(db.String(100),unique=False,nullable=False, default='not started')
    module_2_score= db.Column(db.Integer, default= 0)
    module_2_status = db.Column(db.String(100),unique=False,nullable=False, default='not started')
    module_3_score= db.Column(db.Integer, default= 0)
    module_3_status = db.Column(db.String(100),unique=False,nullable=False, default='not started')
    module_4_score= db.Column(db.Integer, default= 0)
    module_4_status = db.Column(db.String(100),unique=False,nullable=False, default='not started')
    total_score= db.Column(db.Integer, default= 0)
    attention= db.Column(db.Integer, default= 0)
    fluency= db.Column(db.Integer, default= 0)
    language= db.Column(db.Integer, default= 0)
    memory= db.Column(db.Integer, default= 0)
    visuospatial= db.Column(db.Integer, default= 0)
    completed= db.Column(db.Boolean,unique=False,nullable=False, default=False)

    def __repr__(self):
        return '<Test {}>'.format(self.id)


class Module_1(db.Model):
    __tablename__ = "module_1"

    id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True )
    question_1= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_2= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_3= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_4= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_5= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_6= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_7= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_8= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_9= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_10= db.Column(db.Boolean,unique=False,nullable=False, default=False)


    def __repr__(self):
        return '<Module_1 {}>'.format(self.id)

class Module_2(db.Model):
    __tablename__ = "module_2"

    id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True )
    question_1= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_2= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_3= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_4= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_5= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_6= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_7= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_8= db.Column(db.Boolean,unique=False,nullable=False, default=False)


    def __repr__(self):
        return '<Module_2{}>'.format(self.id)

class Module_3(db.Model):
    __tablename__ = "module_3"

    id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True )
    question_1= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_2= db.Column(db.Boolean,unique=False,nullable=False, default=False)
    question_3= db.Column(db.Boolean,unique=False,nullable=False, default=False)

    def __repr__(self):
        return '<Module_3{}>'.format(self.id)

class Module_4(db.Model):
    __tablename__ = "module_4"

    id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True )
    question_1= db.Column(db.Boolean,unique=False,nullable=False, default=False)


    def __repr__(self):
        return '<Module_4{}>'.format(self.id)

db.create_all()

login_manager= LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)

''' code for admin panel'''

class MyModelView(ModelView):
        column_display_pk = True
        


# edits AdminIndexView to only allow users who are logged in as admin to access page. WIll return 404 error if not.
class myAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin
    
    def inaccessible_callback(self, name, **kwargs):    
        return page_not_found(404)


admin = Admin(app, index_view= myAdminIndexView())
admin.add_view(MyModelView(Users, db.session))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))


''' error handlers '''

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

'''csp added to each request, allows scripts and styles from Jquery and Bootstrap, everything else only local files'''
@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy']="default-src 'self'; img-src 'self' ; script-src 'self' https://code.jquery.com/jquery-3.3.1.slim.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js ; style-src 'self' https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css"
    return resp

''' code used to calculate total score '''

def add_score(test):
    total= (test.module_1_score + test.module_2_score + test.module_3_score + test.module_4_score)
    return total

def calculateAge(birthDate):
    today = dt.today()
    age = today.year - birthDate.year 
    if ((today.month, today.day) < (birthDate.month, birthDate.day)):
        age -= 1
    return age

       

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
    country= None
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
            first_name= form.first_name.data.strip(" ")
            form.first_name.data= " "
            last_name= form.last_name.data.strip(" ")
            form.last_name.data= " "
            birthdate= form.birthdate.data.strftime('%d-%m-%Y')
            form.birthdate.data = datetime.strptime("01-01-2020", '%d-%m-%Y')
            email_address= form.email_address.data.lower().strip(" ")
            form.email_address.data= " "
            country= form.country.data
            form.country.data= " "
            password= form.password_hash.data
            form.password_hash.data= " "
            user= Users(first_name= first_name, last_name= last_name, dob= birthdate,
            email_address=email_address,country=country,password_hash=password)
            user.password= password
            db.session.add(user)
            db.session.commit()
        else:
            ''' if user does exist, display message'''
            message= "An account with that email address already exists"
            return render_template("createaccount.html", first_name=first_name,last_name=last_name,birthdate=birthdate,
    email_address=email_address, country=country, password=password, confirm=confirm, accept_tos= accept_tos, form= form,message=message)
    return render_template("createaccount.html", first_name=first_name,last_name=last_name,birthdate=birthdate,
    email_address=email_address,country=country, password=password, confirm=confirm, accept_tos= accept_tos, form= form)
    

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
        user = Users.query.filter_by(email_address=form.email_address.data.lower().strip(" ")).first()
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
    user = current_user
    id = user.id 
    '''check to see if there is an active test'''
    test= Test.query.filter_by(userid= id, completed=False).first()
    if test == None:
        module_1_completed= 'not started'
        module_2_completed= 'not started'
        module_3_completed= 'not started'
        module_4_completed = 'not started'
    else:
        module_1_completed = test.module_1_status
        module_2_completed = test.module_2_status
        module_3_completed= test.module_3_status
        module_4_completed= test.module_4_status
    return render_template("yourgarden.html",module_1_completed= module_1_completed,module_2_completed=module_2_completed,
    module_3_completed=module_3_completed,module_4_completed=module_4_completed)


@app.route('/results')
@login_required
def results():
    user = current_user
    id = user.id 
    all_tests= Test.query.filter_by(userid= id, completed= True).order_by(Test.date_completed).all()
    current_test = Test.query.filter_by(userid= id, completed= False).first()
    module_1 = "not started"
    module_2= "not started"
    module_3 = "not started"
    module_4 = "not started"
    if current_test != None:
        module_1 = current_test.module_1_status 
        module_2 = current_test.module_2_status 
        module_3 = current_test.module_3_status 
        module_4 = current_test.module_4_status 
    incomplete_modules = []
    if module_1 != "completed":
        incomplete_modules.append("Fluency Fountain")
    if module_2 != "completed":
        incomplete_modules.append("Memory Maze")
    if module_3 != "completed":
        incomplete_modules.append("Visual Veg-Plot")
    if module_4 != "completed":
        incomplete_modules.append("Language Log Pile")
    return render_template('results.html',all_tests=all_tests, incomplete_modules=incomplete_modules, current_test=current_test)



@app.route('/account',methods=["GET", "POST"])
@login_required
def account():
    ''' session.pop used to remove 'please login' flash message if user previously navigated to page prior to login'''
    user= current_user
    first_name= user.first_name
    last_name = user.last_name
    birthdate= user.dob
    current_email_address= user.email_address
    country= user.country
    current_password=None
    message= None
    form= EditDetailsForm()
    if form.validate_on_submit():
        first_name= form.first_name.data
        last_name= form.last_name.data
        birthdate= form.birthdate.data
        email_address=form.email_address.data.lower().strip(" ")
        country=form.country.data.strip(" ")
        current_password= form.password_hash.data
        ''' if email address has changed, check that it is not alrady in use '''
        if email_address != current_email_address:
            check = Users.query.filter_by(email_address=email_address).first()
            if check is not None:
                message= "Sorry, please enter a different email address."
                return render_template("account.html", message=message,form=form, user=user, 
                first_name= first_name, last_name= last_name, dob= birthdate,email_address=email_address,country=country,
                password_hash= current_password)   
        '''  check that password entered is correct before updating the details'''
        if user.verify_password(current_password):
            user.first_name= first_name
            user.last_name= last_name
            user.dob= birthdate
            user.email_address= email_address
            user.country=country
            try:
                
                db.session.commit()
                form.first_name.data= user.first_name
                form.last_name.data = user.last_name
                form.birthdate.data= user.dob
                form.email_address.data= user.email_address
                form.country.data= user.country
                message= "Your details have been updated!"
                return render_template("account.html", message=message,form=form, user=user, 
                first_name= first_name, last_name= last_name, dob= birthdate,email_address=email_address,country=country,
                password_hash= current_password)   
            except:
                form.first_name.data= user.first_name
                form.last_name.data = user.last_name
                form.birthdate.data= user.dob
                form.email_address.data= user.email_address
                form.country.data= user.country
                message ="Sorry there was a problem, please try again."
                return render_template("account.html", message=message,form=form, user=user, 
                first_name= first_name, last_name= last_name, dob= birthdate,email_address=email_address,country=country,
                password_hash= current_password)   
        else:
             message= "You entered an incorrect password, please try again."
    return render_template("account.html", message=message,form=form, user=user, first_name= first_name, 
    last_name= last_name, dob= birthdate,email_address=current_email_address,country=country,password_hash= current_password)   

@app.route('/logout')
@login_required
def logout():
    user= current_user
    user.last_seen= datetime.utcnow()
    db.session.commit()
    logout_user()
    return render_template("logout.html")

''' ROUTES FOR MODULE 1 '''

@app.route('/fluency')
@login_required
def fluency():
    user= current_user
    id= user.id
    test= Test.query.filter_by(userid=id).first() 
    '''if this is their first time taking the test, variables set to false'''
    if test is None:
        active_test= False 
        completed = False
        started = False 
    else:
        test = Test.query.filter_by(userid=id, completed= False).first() 
        '''if they have no active tests ongoing'''
        if test is None: 
            active_test= False 
            completed = True
            started= False 
        else:
            active_test= True 
            module_1_status = test.module_1_status
            '''if they have alreay completed module 1''' 
            if module_1_status == 'completed':
                completed= True
                started= False 
            elif module_1_status == "in progress":
                started = True 
                completed = False 
            else:
                completed= False 
                started = False 
    return render_template("/modules/module1/fluency.html", started=started, completed=completed, active_test=active_test)

@app.route('/fluencycontinue')
@login_required
def fluencycontinue():
    user= current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first() 
    '''logic below checks which question they have already completed'''
    if questions.question_10:
        message= "You have completed Fluency Fountain!"
        return render_template("/yourgarden.html", message=message)
    elif questions.question_9:
        return redirect (url_for('fluency10'))
    elif questions.question_8:
        return redirect(url_for('fluency9'))
    elif questions.question_7:
        return redirect(url_for('fluency8'))
    elif questions.question_6:
        return redirect(url_for('fluency7'))
    elif questions.question_5:
        return redirect(url_for('fluency6'))
    elif questions.question_4:
        return redirect(url_for('fluency5'))
    elif questions.question_3:
        return redirect(url_for('fluency4'))
    elif questions.question_2:
        return redirect(url_for('fluency3'))
    elif questions.question_1:
        return redirect(url_for('fluency2'))
    else:
        return redirect(url_for('fluency1'))


@app.route('/fluency1',methods=["GET", "POST"])
@login_required
def fluency1():
    user = current_user
    id= user.id
    test= Test.query.filter_by(userid= id, completed=False).first()
    if test == None:
        module_1= Module_1.query.filter_by(id= id).first()
        if module_1 == None:
            test = Test(userid=id)
            module_1= Module_1(id=id)
            db.session.add(test)
            db.session.add(module_1)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_1.query.filter_by(id= id).first()
        else:
            module_1.question_1 = False
            module_1.question_2 = False 
            module_1.question_3 = False 
            module_1.question_4 = False 
            module_1.question_5 = False 
            module_1.question_6 = False 
            module_1.question_7 = False 
            module_1.question_8 = False 
            module_1.question_9 = False 
            module_1.question_10 = False
            test = Test(userid=id)
            db.session.add(test)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_1.query.filter_by(id= id).first() 
    else:
        module_1= Module_1.query.filter_by(id= id).first()
        if module_1 == None:
            module_1= Module_1(id=id)
            db.session.add(module_1)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_1.query.filter_by(id= id).first()
        else:
            module_1.question_1 = False
            module_1.question_2 = False 
            module_1.question_3 = False 
            module_1.question_4 = False 
            module_1.question_5 = False 
            module_1.question_6 = False 
            module_1.question_7 = False 
            module_1.question_8 = False 
            module_1.question_9 = False 
            module_1.question_10 = False
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_1.query.filter_by(id= id).first()
    if questions.question_1:
        return redirect(url_for('yourgarden'))
    day = None
    date= None
    month= None
    year= None
    season= None
    birthdate=None
    email_address= None
    test_place= None
    age= None
    country= None
    message= None
    next= None
    form = Fluency_1()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        '''status changed to in progress as module has been started'''
        test.module_1_status='in progress'
        module_score= test.module_1_score
        attention= test.attention
        day = form.day.data
        date= form.date.data
        month= form.month.data
        year= form.year.data
        season= form.season.data
        birthdate= form.birthdate.data
        email_address= form.email_address.data
        test_place= form.test_place.data
        age= int(form.age.data)
        country= form.country.data
        actual_date= dt.today()
        actual_day= actual_date.day
        actual_year= actual_date.year
        day_now= calendar.day_name[actual_date.weekday()]
        month_now = str(calendar.month_name[actual_date.month])
        winter= ["November","December", "January", "February"]
        spring= ["March", "April", "May","June"]
        summer= ["June", "July", "August","September"]
        autumn= ["September", "October", "November"]
        actual_birthdate= user.dob
        print("birthdays",birthdate,actual_birthdate)
        actual_email = user.email_address
        actual_age= calculateAge(actual_birthdate)
        actual_country= user.country
        print ("ages", age, actual_age)
        if day == day_now:
            print("day is correct")
            attention += 1 
            module_score +=1
        print(day)
        print(day_now)
        if int(date) in range((actual_day-2),(actual_day+2)):
            print("date is correct")
            attention += 1
            module_score +=1
        print(date)
        print(actual_day)
        if month == month_now:
            print("month is correct")
            attention += 1
            module_score +=1
        print(month)
        print(month_now)
        if int(year) == actual_year:
            print("year is correct")
            attention += 1
            module_score +=1
            type(year)
        print(year)
        print(actual_year)
        if season == "Winter":
            if month_now in winter:
                print("season is correct")
                attention += 1
                module_score +=1
            else:
                pass
        elif season == "Spring":
            if month_now in spring:
                print("season is correct")
                attention += 1
                module_score +=1
            else:
                pass
        elif season == "Summer":
            if month_now in summer:
                print("season is correct")
                attention += 1
                module_score +=1
            else:
                pass
        elif season == "Autumn":
            if month_now in autumn:
                print("season is correct")
                attention += 1
                module_score +=1
            else:
                pass
        if birthdate == actual_birthdate:
            attention += 1
            module_score +=1
            print("birthdate is correct")
        else:
            pass
        if email_address == actual_email:
            attention += 1
            module_score +=1
            print("email is correct")
        else:
            pass
        if test_place.lower() == 'fluency fountain':
            attention += 1
            module_score +=1
            print("test p is correct")
        else:
            pass
        if age == actual_age:
            attention += 1
            module_score +=1
            print("age is correct")
        else:
            pass
        if country == actual_country:
            attention += 1
            module_score +=1
            print("country is correct")
        else:
            pass
        test.module_1_score= module_score
        test.attention= attention
        print("attention socre is", test.attention)
        questions.question_1= True
        db.session.commit()
        return render_template("/modules/module1/fluency1completed.html")
    return render_template("/modules/module1/fluency1.html", day= day, date= date, year= year, season= season,birthdate=birthdate,
    email_address= email_address, test_place=test_place, age= age, country= country,form=form,next=next,message= message)



@app.route('/fluency2',methods=["GET", "POST"])
@login_required
def fluency2():
    user= current_user 
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    if questions.question_2:
        return redirect(url_for('yourgarden'))
    if not questions.question_1:
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    message= None
    next= None
    form= Fluency_2()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        attention= test.attention
        value_1 = form.v1.data
        value_2 = form.v2.data
        value_3 = form.v3.data
        answers_1= ["lemon","leman","liman","limon"]
        answers_2= ["key","kee","ki","kie"]
        answers_3= ["ball","bal","baul"]
        if value_1.lower() in answers_1:
            module_score += 1
            attention += 1 
        if value_2.lower() in answers_2:
            module_score += 1
            attention += 1 
        if value_3.lower() in answers_3:
            module_score += 1
            attention += 1 
        test.attention= attention
        test.module_1_score= module_score
        questions.question_2= True
        db.session.commit()
        message= "Your answers have been accepted, please click next to continue"
        next= True
        return render_template("/modules/module1/fluency2.html", value_1=value_1,value_2=value_2,value_3=value_3,
        form=form,message= message, next= next)
    return render_template("/modules/module1/fluency2.html",value_1=value_1,value_2=value_2,value_3=value_3,
        form=form,message= message, next= next)
    



@app.route('/fluency3',methods=["GET", "POST"])
@login_required
def fluency3():
    user= current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    if questions.question_3:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2:
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    value_4 = None
    value_5 = None
    message= None
    next= None
    form= Fluency_3()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        attention= test.attention
        value_1 = form.v1.data
        value_2 = form.v2.data
        value_3 = form.v3.data
        value_4 = form.v4.data
        value_5 = form.v5.data
        if value_1 == 93:
            module_score += 1
            attention += 1 
        if value_2 == 86:
            module_score += 1
            attention += 1 
        if value_3 == 79:
            module_score += 1
            attention += 1 
        if value_4 == 72:
            module_score += 1
            attention += 1 
        if value_5 == 65:
            module_score += 1
            attention += 1     
        test.module_1_score= module_score
        test.attention= attention
        questions.question_3= True
        db.session.commit()
        message= "Your answers have been accepted, please click next to continue"
        next= True
        return render_template("/modules/module1/fluency3.html", value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,value_5=value_5,form=form,message= message, next= next)
    return render_template("/modules/module1/fluency3.html",value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,value_5=value_5,form=form,message= message, next= next)

@app.route('/fluency4',methods=["GET", "POST"])
@login_required
def fluency4():
    user = current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    if questions.question_4:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3:
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    message= None
    next= None
    form= Fluency_2()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        memory= test.memory
        value_1 = form.v1.data.strip(" ")
        value_2 = form.v2.data.strip(" ")
        value_3 = form.v3.data.strip(" ")
        answers_1= ["lemon","leman","liman","limon"]
        answers_2= ["key","kee","ki","kie"]
        answers_3= ["ball","bal","baul"]
        if value_1.lower() in answers_1:
            module_score += 1
            memory += 1 
        if value_2.lower() in answers_2:
            module_score += 1
            memory += 1 
        if value_3.lower() in answers_3:
            module_score += 1
            memory += 1 
        test.memory= memory
        test.module_1_score= module_score
        questions.question_4= True
        db.session.commit()
        message= "Your answers have been accepted, please click next to continue"
        next= True
        return render_template("/modules/module1/fluency4.html", value_1=value_1,value_2=value_2,value_3=value_3,
        form=form,message= message, next= next)
    return render_template("/modules/module1/fluency4.html",value_1=value_1,value_2=value_2,value_3=value_3,
        form=form,message= message, next= next)
    

@app.route('/fluency5',methods=["GET", "POST"])
@login_required
def fluency5():
    user= current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    if questions.question_5:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3 or not questions.question_4 :
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    value_4 = None
    message= None
    next= None
    form= Fluency_5()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        memory= test.memory
        value_1 = form.v1.data.strip(" ")
        value_2 = form.v2.data.strip(" ")
        value_3 = form.v3.data.strip(" ")
        value_4 = form.v4.data.strip(" ")
        q1_answers=["johnson","jonson", "jonsan", "boris johnson","boris jonson","boris jonsan", 
        "borris johnson", "borris jonson","borris jonsan"]
        q2_answers=["thatcher","thacher", "thatchar", "thachar", "margaret thatcher", "margaret thacher", "margaret thatchar",
        "mrgaret thachar", "margarat thatcher", "margarat thacher", "margarat thatchar", "margarat thachar"]
        q3_answers=["biden","bidon","bidan", "bydon","byden","bydan", "joe biden","joe bidon", "joe bidan", "joe bydon","joe byden",
        "joe bydan", "joseph biden","joeseph bidon", "joeseph bidan", "joeseph byden","joeseph bydon", "joeseph bydan", "jo biden",
        "jo bidon", "jo bidan", "jo byden", "jo bydon", "jo bydan"]
        q4_answers=["kennedy","kenedy", "kenady","john kennedy","john f. kennedy","john f kennedy", "jon kennedy", "jon f. kennedy", 
        "jon f kennedy", "kenedy","john kenedy","john f. kenedy", "john f kenedy", "jon kenedy", "jon f. kenedy", "jon f kenedy", 
        "john kenady", "john f. kenady", "john f kenady", "jon kenady", "jon f. kenady", "jon f kenady"]
        if value_1.lower() in q1_answers:
            module_score += 1
            memory += 1 
        if value_2.lower() in q2_answers:
            module_score += 1
            memory += 1
        if value_3.lower() in q3_answers:
            module_score += 1
            memory += 1
        if value_4.lower() in q4_answers:
            module_score += 1
            memory += 1
        test.memory= memory
        test.module_1_score= module_score
        questions.question_5 = True
        db.session.commit()
        message= "Your answers have been accepted, please click next to continue"
        next= True
        return render_template("/modules/module1/fluency5.html", value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,form=form,message= message, next= next)
    return render_template("/modules/module1/fluency5.html",value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,form=form,message= message, next= next)
    

@app.route('/fluency6',methods=["GET", "POST"])
@login_required
def fluency6():
    user= current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    if questions.question_6:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3 or not questions.question_4 or not questions.question_5 :
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    value_4 = None
    form= Fluency_6()
    if form.validate_on_submit():
        user= current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        language= test.language
        value_1 = form.v1.data
        value_2 = form.v2.data
        value_3 = form.v3.data
        value_4 = form.v4.data
        total = (value_1 + value_2 + value_3 + value_4)
        module_score += total
        language += total 
        test.language= language
        test.module_1_score= module_score
        questions.question_6=True
        db.session.commit()
        return render_template("/modules/module1/fluency6completed.html")
    return render_template("/modules/module1/fluency6.html", form= form, value_1=value_1, value_2=value_2, value_3= value_3,
    value_4=value_4)

@app.route('/fluency7',methods=["GET", "POST"])
@login_required
def fluency7():
    user= current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    if questions.question_7:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3 or not questions.question_4 or not questions.question_5 or not questions.question_6 :
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    value_4 = None
    value_5 = None
    value_6 = None
    value_7 = None
    value_8 = None
    value_9 = None
    value_10 = None
    value_11 = None
    value_12 = None
    message= None
    next= None
    form= Fluency_7()
    if form.validate_on_submit():
        user= current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        questions.question_7=True
        module_score= test.module_1_score
        language= test.language
        value_1 = form.v1.data.strip(" ")
        value_2 = form.v2.data.strip(" ")
        value_3 = form.v3.data.strip(" ")
        value_4 = form.v4.data.strip(" ")
        value_5 = form.v5.data.strip(" ")
        value_6 = form.v6.data.strip(" ")
        value_7 = form.v7.data.strip(" ")
        value_8 = form.v8.data.strip(" ")
        value_9 = form.v9.data.strip(" ")
        value_10 = form.v10.data.strip(" ")
        value_11 = form.v11.data.strip(" ")
        value_12 = form.v12.data.strip(" ")
        q1_answers=["spoon"]
        q2_answers=["book"]
        q3_answers=["kangaroo","kangaro","kangeroo","kangero","walaby","waleby","wallaby","walleby"]
        q4_answers=["penguin","pengin","pengun","pegine","pengune"]
        q5_answers=["anchor","ancher","anchar","ancer","ancar","ancor"]
        q6_answers=["camel","dromedary","camal","cammel","cammal","camle","cammle"]
        q7_answers=["harp"]
        q8_answers=["rhino","rhinoceros","ryno","rino","rinoserous","rinocerous","rinoseros","rinoceros","rhinocerous","rhinoserous"]
        q9_answers=["barrel","keg","tub","barel","barall","baral"]
        q10_answers=["crown"]
        q11_answers=["crocodile","alligator","crocadile","crocerdile", "alligater", "alligatar", "aligator", "aligater", "aligatar"]
        q12_answers=["piano accordion","accordian","squeeze box","acordian","piano acordian"]
        if value_1.lower() in q1_answers:
            module_score += 1
            language += 1 
            print("q1 right")
        if value_2.lower() in q2_answers:
            module_score += 1
            language += 1 
        if value_3.lower() in q3_answers:
            module_score += 1
            language += 1 
        if value_4.lower() in q4_answers:
            module_score += 1
            language += 1 
        if value_5.lower() in q5_answers:
            module_score += 1
            language += 1 
        if value_6.lower() in q6_answers:
            module_score += 1
            language+= 1 
        if value_7.lower() in q7_answers:
            module_score += 1
            language+= 1 
        if value_8.lower() in q8_answers:
            module_score += 1
            language += 1 
        if value_9.lower() in q9_answers:
            module_score += 1
            language += 1 
        if value_10.lower() in q10_answers:
            module_score += 1
            language += 1 
        if value_11.lower() in q11_answers:
            module_score += 1
            language += 1 
        if value_12.lower() in q12_answers:
            module_score += 1
            language += 1 
        test.language= language
        test.module_1_score= module_score
        questions.question_7 = True
        db.session.commit()
        message= "Your answers have been accepted, please click next to continue"
        next= True
        return render_template("/modules/module1/fluency7.html", value_1 =value_1, value_2 = value_2,value_3 = value_3,value_4=value_4,
    value_5 = value_5, value_6 = value_6, value_7 = value_7, value_8 = value_8, value_9 = value_9, value_10 = value_10,value_11 = value_11,
    value_12 = value_12, message= message,next= next,form= form)
    return render_template("/modules/module1/fluency7.html", value_1 =value_1, value_2 = value_2,value_3 = value_3,value_4=value_4,
    value_5 = value_5, value_6 = value_6, value_7 = value_7, value_8 = value_8, value_9 = value_9, value_10 = value_10,value_11 = value_11,
    value_12 = value_12, message= message,next= next,form= form)
          


@app.route('/fluency8',methods=["GET", "POST"])
@login_required
def fluency8():
    user= current_user
    id= user.id
    question= Module_1.query.filter_by(id= id).first()
    '''used to stop users skipping back'''
    if question.question_8:
        return redirect(url_for('yourgarden'))
    ''' used to stop users skipping forward'''
    if not question.question_1 or not question.question_2 or not question.question_3 or not question.question_4 or not question.question_5 or not question.question_6 or not question.question_7:
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    value_4 = None
    message= None
    next= None
    form= Fluency_8()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        language= test.language
        value_1 = int(form.v1.data)
        value_2 = int(form.v2.data)
        value_3 = int(form.v3.data)
        value_4 = int(form.v4.data)
        if value_1 == 10:
            module_score += 1
            language += 1 
            print("q1 right")
        if value_2 == 3:
            module_score += 1
            language += 1
        if value_3 == 4:
            module_score += 1
            language += 1
        if value_4 == 5:
            module_score += 1
            language += 1
        test.language= language
        test.module_1_score= module_score
        questions.question_8 = True
        db.session.commit()
        message= "Your answers have been accepted, please click next to continue"
        next= True
        return render_template("/modules/module1/fluency8.html", value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,form=form,message= message, next= next)
    return render_template("/modules/module1/fluency8.html",value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,form=form,message= message, next= next)


@app.route('/fluency9',methods=["GET", "POST"])
@login_required
def fluency9():
    user= current_user
    id= user.id
    question= Module_1.query.filter_by(id= id).first()
    if question.question_9:
        return redirect(url_for('yourgarden'))
    if not question.question_1 or not question.question_2 or not question.question_3 or not question.question_4 or not question.question_5 or not question.question_6 or not question.question_7 or not question.question_8:
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    value_4 = None
    message= None
    next= None
    form= Fluency_9()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        visuospatial= test.visuospatial
        value_1 = int(form.v1.data)
        value_2 = int(form.v2.data)
        value_3 = int(form.v3.data)
        value_4 = int(form.v4.data)
        if value_1 == 8:
            module_score += 1
            visuospatial += 1 
            print("q1 right")
        if value_2 == 10:
            module_score += 1
            visuospatial += 1
        if value_3 == 7:
            module_score += 1
            visuospatial += 1
        if value_4 == 9:
            module_score += 1
            visuospatial += 1
        test.visuospatial= visuospatial
        test.module_1_score= module_score
        questions.question_9 = True
        db.session.commit()
        message= "Your answers have been accepted, please click next to continue"
        next= True
        return render_template("/modules/module1/fluency9.html", value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,form=form,message= message, next= next)
    return render_template("/modules/module1/fluency9.html",value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,form=form,message= message, next= next)

@app.route('/fluency10',methods=["GET", "POST"])
@login_required
def fluency10():
    user= current_user
    id= user.id
    question= Module_1.query.filter_by(id= id).first()
    if question.question_10:
        return redirect(url_for('yourgarden'))
    if not question.question_1 or not question.question_2 or not question.question_3 or not question.question_4 or not question.question_5 or not question.question_6 or not question.question_7 or not question.question_8 or not question.question_9:
        return redirect(url_for('yourgarden'))
    value_1 = None
    value_2 = None
    value_3 = None
    value_4 = None
    message= None
    next= None
    form= Fluency_10()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        visuospatial= test.visuospatial
        value_1 = form.v1.data.strip(" ")
        value_2 = form.v2.data.strip(" ")
        value_3 = form.v3.data.strip(" ")
        value_4 = form.v4.data.strip(" ")
        if value_1.upper() == "K":
            module_score += 1
            visuospatial += 1 
            print("q1 right")
        if value_2.upper() == "M":
            module_score += 1
            visuospatial += 1
        if value_3.upper() == "A":
            module_score += 1
            visuospatial += 1
        if value_4.upper() == "T":
            module_score += 1
            visuospatial += 1
        test.visuospatial= visuospatial
        test.module_1_score= module_score
        test.total_score = add_score(test)
        test.module_1_status= 'completed'
        module_2_completed= test.module_2_status
        module_3_completed= test.module_3_status
        module_4_completed= test.module_4_status
        if module_2_completed == module_3_completed == module_4_completed == 'completed':
            test.completed= True 
            test.date_completed= datetime.utcnow() 
        questions.question_10 = True
        db.session.commit()
        message= "Your answers have been accepted, thank you for completing Fluency Fointain! Please click next to continue"
        next= True
        return render_template("/modules/module1/fluency10.html", value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,form=form,message= message, next= next)
    return render_template("/modules/module1/fluency10.html",value_1=value_1,value_2=value_2,value_3=value_3,
        value_4=value_4,form=form,message= message, next= next)


''' ROUTES FOR MODULE 2 '''

@app.route('/memory')
@login_required
def memory():
    user= current_user
    id= user.id
    test= Test.query.filter_by(userid=id).first() 
    '''if this is their first time taking the test, variables set to false'''
    if test is None:
        active_test= False 
        completed = False
        started= False 
    else:
        test = Test.query.filter_by(userid=id, completed= False).first() 
        '''if they have no active tests ongoing'''
        if test is None: 
            completed = True
            active_test= False 
            started = False 
        else:
            active_test= True 
            module_2_status = test.module_2_status
            '''if they have already completed module 2''' 
            if module_2_status == 'completed':
                completed= True
                started = False 
            elif module_2_status == "in progress":
                started = True 
                completed = False 
            else:
                completed= False 
                started = False 
    return render_template("/modules/module2/memory.html", completed=completed, started= started, active_test=active_test)

@app.route('/memorycontinue')
@login_required
def memorycontinue():
    user= current_user
    id= user.id
    questions= Module_2.query.filter_by(id= id).first() 
    '''logic below checks which question they have already completed'''
    if questions.question_8:
        message= "You have completed Memory Maze!"
        return render_template("/yourgarden.html", message=message)
    elif questions.question_7:
        return redirect(url_for('memory8'))
    elif questions.question_6:
        return redirect(url_for('memory7'))
    elif questions.question_5:
        return redirect(url_for('memory6'))
    elif questions.question_4:
        return redirect(url_for('memory5'))
    elif questions.question_3:
        return redirect(url_for('memory4'))
    elif questions.question_2:
        return redirect(url_for('memory3'))
    elif questions.question_1:
        return redirect(url_for('memory2'))
    else:
        return redirect(url_for('memory1'))



@app.route('/memory1')
@login_required
def memory1():
    user = current_user
    id= user.id
    test= Test.query.filter_by(userid= id, completed=False).first()
    '''if there is no active test'''
    if test == None:
        module_2= Module_2.query.filter_by(id= id).first()
        ''' if there is no entry on module 2 for given user id, add one and create new Test'''
        if module_2 == None:
            test = Test(userid=id)
            module_2= Module_2(id=id)
            db.session.add(test)
            db.session.add(module_2)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_2.query.filter_by(id= id).first()
        else:
            '''if there is an entry for user id on module 2, reset questions to False and create new Test'''
            module_2.question_1 = False
            module_2.question_2 = False 
            module_2.question_3 = False 
            module_2.question_4 = False 
            module_2.question_5 = False 
            module_2.question_6 = False 
            module_2.question_7 = False 
            module_2.question_8 = False 
            test = Test(userid=id)
            db.session.add(test)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_2.query.filter_by(id= id).first() 
    else:
        '''if there is an active test, check if there is an entry on module 2 for user ID '''
        module_2= Module_2.query.filter_by(id= id).first()
        if module_2 == None:
            '''if there is no entry on module 2, create one and load active test'''
            module_2= Module_2(id=id)
            db.session.add(module_2)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_2.query.filter_by(id= id).first()
        else:
            '''if there is, set module 2 questions to false and load active test'''
            module_2.question_1 = False
            module_2.question_2 = False 
            module_2.question_3 = False 
            module_2.question_4 = False 
            module_2.question_5 = False 
            module_2.question_6 = False 
            module_2.question_7 = False 
            module_2.question_8 = False 
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_2.query.filter_by(id= id).first()
    if questions.question_1:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation here'''
    user = current_user
    id= user.id
    test= Test.query.filter_by(userid= id, completed= False).first()
    questions= Module_2.query.filter_by(id= id).first()
    '''status changed to in progress as module has been started'''
    test.module_2_status='in progress'
    module_score= test.module_2_score
    fluency= test.fluency
    '''add question checking and score adding here, adding to module_score and fluency or not if incorrect'''
    test.module_2_score= module_score
    test.fluency= fluency
    questions.question_1= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module2/memory1.html", message= message, next= next)


@app.route('/memory2')
@login_required
def memory2():
    user = current_user
    id= user.id
    questions= Module_2.query.filter_by(id= id).first()
    if questions.question_2:
        return redirect(url_for('yourgarden'))
    if not questions.question_1:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_2_score
    fluency= test.fluency
    '''add question checking and score adding here, adding to module_score and fluency or not if incorrect'''
    test.module_2_score= module_score
    test.fluency= fluency
    questions.question_2= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module2/memory2.html", message= message, next= next)

@app.route('/memory3')
@login_required
def memory3():
    user = current_user
    id= user.id
    questions= Module_2.query.filter_by(id= id).first()
    if questions.question_3:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_2_score
    memory= test.memory
    '''add question checking and score adding here, adding to module_score and memory, or not if incorrect'''
    test.module_2_score= module_score
    test.memory= memory
    questions.question_3= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module2/memory3.html", message= message, next= next)

@app.route('/memory4')
@login_required
def memory4():
    user = current_user
    id= user.id
    questions= Module_2.query.filter_by(id= id).first()
    if questions.question_4:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation here'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_2_score
    language= test.language
    '''add question checking and score adding here, adding to module_score and language, or not if incorrect'''
    test.module_2_score= module_score
    test.language= language
    questions.question_4= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module2/memory4.html", message= message, next= next)

@app.route('/memory5')
@login_required
def memory5():
    user = current_user
    id= user.id
    questions= Module_2.query.filter_by(id= id).first()
    if questions.question_5:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3 or not questions.question_4:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation here'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_2_score
    language= test.language
    '''add question checking and score adding here, adding to module_score and language, or not if incorrect'''
    test.module_2_score= module_score
    test.language= language
    questions.question_5= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module2/memory5.html", message= message, next= next)

@app.route('/memory6')
@login_required
def memory6():
    user = current_user
    id= user.id
    questions= Module_2.query.filter_by(id= id).first()
    if questions.question_6:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3 or not questions.question_4 or not questions.question_5:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation here'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_2_score
    language= test.language
    '''add question checking and score adding here, adding to module_score and language, or not if incorrect'''
    test.module_2_score= module_score
    test.language= language
    questions.question_6= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module2/memory6.html", message= message, next= next)

@app.route('/memory7')
@login_required
def memory7():
    user = current_user
    id= user.id
    questions= Module_2.query.filter_by(id= id).first()
    if questions.question_7:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3 or not questions.question_4 or not questions.question_5 or not questions.question_6:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation here'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_2_score
    language= test.language
    '''add question checking and score adding here, adding to module_score and language, or not if incorrect'''
    test.module_2_score= module_score
    test.language= language
    questions.question_7= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module2/memory7.html", message= message, next= next)

@app.route('/memory8')
@login_required
def memory8():
    user = current_user
    id= user.id
    questions= Module_2.query.filter_by(id= id).first()
    if questions.question_8:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2 or not questions.question_3 or not questions.question_4 or not questions.question_5 or not questions.question_6 or not questions.question_7:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_2_score
    memory= test.memory
    '''add question checking and score adding here, adding to module_score and memory, or not if incorrect'''
    test.module_2_score= module_score
    test.memory=  memory
    questions.question_8= True
    test.total_score = add_score(test)
    test.module_2_status= 'completed'
    module_1_completed= test.module_1_status
    module_3_completed= test.module_3_status
    module_4_completed= test.module_4_status
    if module_1_completed == module_3_completed == module_4_completed == 'completed':
        test.completed= True 
        test.date_completed= datetime.utcnow() 
    db.session.commit()
    message= "Your answers have been accepted, thank you for completing Memory Maze! Please click to return to your garden"
    next= True
    return render_template("/modules/module2/memory8.html", message= message, next= next)

'''module 3 code '''


@app.route('/visual')
@login_required
def visual():
    user= current_user
    id= user.id
    test= Test.query.filter_by(userid=id).first() 
    '''if this is their first time taking the test, variables set to false'''
    if test is None:
        active_test= False 
        completed = False
        started= False 
    else:
        test = Test.query.filter_by(userid=id, completed= False).first() 
        '''if they have no active tests ongoing'''
        if test is None: 
            completed = True
            active_test= False 
            started = False 
        else:
            active_test= True 
            module_3_status = test.module_3_status
            '''if they have already completed module 3''' 
            if module_3_status == 'completed':
                completed= True
                started = False 
            elif module_3_status == "in progress":
                started = True 
                completed = False 
            else:
                completed= False 
                started = False 
    return render_template("/modules/module3/visual.html", completed=completed, started= started, active_test=active_test)

@app.route('/visualcontinue')
@login_required
def visualcontinue():
    user= current_user
    id= user.id
    questions= Module_3.query.filter_by(id= id).first() 
    '''logic below checks which question they have already completed'''
    if questions.question_3:
        message= "You have completed Visual Veg Plot!"
        return render_template("/yourgarden.html", message=message)
    elif questions.question_2:
        return redirect(url_for('visual3'))
    elif questions.question_1:
        return redirect(url_for('visual2'))
    else:
        return redirect(url_for('visual1'))



@app.route('/visual1')
@login_required
def visual1():
    user = current_user
    id= user.id
    test= Test.query.filter_by(userid= id, completed=False).first()
    if test == None:
        module_3= Module_3.query.filter_by(id= id).first()
        if module_3 == None:
            test = Test(userid=id)
            module_3= Module_3(id=id)
            db.session.add(test)
            db.session.add(module_3)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_3.query.filter_by(id= id).first()
        else:
            module_3.question_1 = False
            module_3.question_2 = False 
            module_3.question_3 = False 
            test = Test(userid=id)
            db.session.add(test)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_3.query.filter_by(id= id).first() 
    else:
        module_3= Module_3.query.filter_by(id= id).first()
        if module_3 == None:
            module_3= Module_3(id=id)
            db.session.add(module_3)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_3.query.filter_by(id= id).first()
        else:
            test= Test.query.filter_by(userid= id,completed=False).first()
            module_3.question_1 = False
            module_3.question_2 = False 
            module_3.question_3 = False 
            questions= Module_3.query.filter_by(id= id).first()
    if questions.question_1:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation here'''
    user = current_user
    id= user.id
    test= Test.query.filter_by(userid= id, completed= False).first()
    questions= Module_3.query.filter_by(id= id).first()
    '''status changed to in progress as module has been started'''
    test.module_3_status='in progress'
    module_score= test.module_3_score
    visuospatial= test.visuospatial
    '''add question checking and score adding here, adding to module_score and fluency or not if incorrect'''
    test.module_3_score= module_score
    test.visuospatial=  visuospatial
    questions.question_1= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module3/visual1.html", message= message, next= next)


@app.route('/visual2')
@login_required
def visual2():
    user = current_user
    id= user.id
    questions= Module_3.query.filter_by(id= id).first()
    if questions.question_2:
        return redirect(url_for('yourgarden'))
    if not questions.question_1:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_3_score
    visuospatial= test.visuospatial
    '''add question checking and score adding here, adding to module_score and fluency or not if incorrect'''
    test.module_3_score= module_score
    test.visuospatial=  visuospatial
    questions.question_2= True
    db.session.commit()
    message= "Your answers have been accepted, please click next to continue"
    next= True
    return render_template("/modules/module3/visual2.html", message= message, next= next)

@app.route('/visual3')
@login_required
def visual3():
    user = current_user
    id= user.id
    questions= Module_3.query.filter_by(id= id).first()
    if questions.question_3:
        return redirect(url_for('yourgarden'))
    if not questions.question_1 or not questions.question_2:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_3_score
    visuospatial= test.visuospatial
    '''add question checking and score adding here, adding to module_score and memory, or not if incorrect'''
    test.module_3_score= module_score
    test.visuospatial= visuospatial
    questions.question_3= True
    test.total_score = add_score(test)
    test.module_3_status= 'completed'
    module_1_completed= test.module_1_status
    module_2_completed= test.module_2_status
    module_4_completed= test.module_4_status
    if module_1_completed == module_2_completed == module_4_completed == 'completed':
        test.completed= True 
        test.date_completed= datetime.utcnow() 
    db.session.commit()
    message= "Your answers have been accepted, thank you for completing Visual Veg Plot! Please click next to return to your garden."
    next= True
    return render_template("/modules/module3/visual3.html", message= message, next= next)



'''code for module 4 '''

@app.route('/language')
@login_required
def language():
    user= current_user
    id= user.id
    test= Test.query.filter_by(userid=id).first() 
    '''if this is their first time taking the test, variables set to false'''
    if test is None:
        active_test= False 
        completed = False
        started= False 
    else:
        test = Test.query.filter_by(userid=id, completed= False).first() 
        '''if they have no active tests ongoing'''
        if test is None: 
            completed = True
            active_test= False 
            started = False 
        else:
            active_test= True 
            module_4_status = test.module_4_status
            '''if they have already completed module 4''' 
            if module_4_status == 'completed':
                completed= True
                started = False 
            elif module_4_status == "in progress":
                started = True 
                completed = False 
            else:
                completed= False 
                started = False 
    return render_template("/modules/module4/language.html", completed=completed, started= started, active_test=active_test)


@app.route('/language1')
@login_required
def language1():
    user = current_user
    id= user.id
    test= Test.query.filter_by(userid= id, completed=False).first()
    if test == None:
        module_4= Module_4.query.filter_by(id= id).first()
        if module_4 == None:
            test = Test(userid=id)
            module43= Module_4(id=id)
            db.session.add(test)
            db.session.add(module_4)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_3.query.filter_by(id= id).first()
        else:
            module_4.question_1 = False
            test = Test(userid=id)
            db.session.add(test)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_4.query.filter_by(id= id).first() 
    else:
        module_4= Module_4.query.filter_by(id= id).first()
        if module_4 == None:
            module_4= Module_4(id=id)
            db.session.add(module_4)
            db.session.commit()
            test= Test.query.filter_by(userid= id,completed=False).first()
            questions= Module_3.query.filter_by(id= id).first()
        else:
            test= Test.query.filter_by(userid= id,completed=False).first()
            module_4.question_1 = False
            questions= Module_4.query.filter_by(id= id).first()
    if questions.question_1:
        return redirect(url_for('yourgarden'))
    message= None
    next= None
    '''add if form validation'''
    user = current_user
    test= Test.query.filter_by(userid= id, completed= False).first()
    module_score= test.module_4_score
    language= test.language
    '''add question checking and score adding here, adding to module_score and memory, or not if incorrect'''
    test.module_4_score= module_score
    test.language= language
    questions.question_1= True
    test.total_score = add_score(test)
    test.module_4_status= 'completed'
    module_1_completed= test.module_1_status
    module_2_completed= test.module_2_status
    module_3_completed= test.module_3_status
    if module_1_completed == module_2_completed == module_3_completed == 'completed':
        test.completed= True 
        test.date_completed= datetime.utcnow() 
    db.session.commit()
    message= "Your answers have been accepted, thank you for completing Laguage Log Pile! Please click next to continue"
    next= True
    return render_template("/modules/module4/language1.html", message= message, next=next)



if __name__ == '__main__':
    app.run(port=80, debug=True)
   

    