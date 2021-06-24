from hashlib import new
from re import L
from flask import Flask, flash, jsonify, request, url_for, jsonify, session, render_template, make_response, redirect, render_template, abort
from datetime import datetime, timedelta, date as dt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_migrate import Migrate, current
from sqlalchemy.sql.schema import DEFAULT_NAMING_CONVENTION
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
import os
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from forms import LoginForm,CreateAccountForm,ResetPasswordForm,ForgottenPasswordForm, EditDetailsForm,LoggedInResetPasswordForm,AdminEditForm
from fluency_forms import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import calendar



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

    id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True )
    module_1_score= db.Column(db.Integer, default= 0)
    module_2_score= db.Column(db.Integer, default= 0)
    module_3_score= db.Column(db.Integer, default= 0)
    module_4_score= db.Column(db.Integer, default= 0)
    total_score= db.Column(db.Integer, default= 0)
    attention= db.Column(db.Integer, default= 0)
    fluency= db.Column(db.Integer, default= 0)
    language= db.Column(db.Integer, default= 0)
    memory= db.Column(db.Integer, default= 0)
    visuospatial= db.Column(db.Integer, default= 0)

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


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


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
            user= Users(first_name= first_name, last_name= last_name, dob= birthdate,
            email_address=email_address,password_hash=password)
            user.password= password
            db.session.add(user)
            db.session.commit()
            id = str(user.id) 
            test = Test(id= id)
            module_1= Module_1(id=id)
            module_2= Module_2(id=id)
            module_3= Module_3(id=id)
            module_4= Module_4(id=id)
            db.session.add(test)
            db.session.commit()
            db.session.add(module_1)
            db.session.commit()
            db.session.add(module_2)
            db.session.commit()
            db.session.add(module_3)
            db.session.commit()
            db.session.add(module_4)
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
        user = Users.query.filter_by(email_address=form.email_address.data.strip(" ")).first()
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
    current_email_address= user.email_address
    current_password=None
    message= None
    form= EditDetailsForm()
    if form.validate_on_submit():
        first_name= form.first_name.data
        last_name= form.last_name.data
        birthdate= form.birthdate.data
        email_address=form.email_address.data.lower()
        current_password= form.password_hash.data
        ''' if email address has changed, check that it is not alrady in use '''
        if email_address != current_email_address:
            check = Users.query.filter_by(email_address=email_address).first()
            if check is not None:
                message= "Sorry, please enter a different email address."
                return render_template("account.html", message=message,form=form, user=user, 
                first_name= first_name, last_name= last_name, dob= birthdate,email_address=email_address,
                password_hash= current_password)   
        '''  check that password entered is correct before updating the details'''
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
    last_name= last_name, dob= birthdate,email_address=current_email_address,password_hash= current_password)   

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
    try:
        db.session.delete(update_user)
        db.session.commit()
        all_users=  Users.query.order_by(Users.date_created)
        flash("User has been deleted!")
        return render_template("admin.html", all_users=all_users)
    except:
        flash("There was a problem, please try again.")
        return render_template("admin.html", all_users=all_users)

''' ROUTES FOR MODULE 1 '''

@app.route('/fluency')
@login_required
def fluency():
    user= current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    question_1= questions.question_1
    return render_template("/modules/module1/fluency.html",questions_1= question_1)

@app.route('/fluencycontinue')
@login_required
def fluencycontinue():
    user= current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first() 
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


@app.route('/fluency1',methods=["GET", "POST"])
@login_required
def fluency1():
    user = current_user
    id= user.id
    test= Test.query.filter_by(id= id).first()
    test.module_1_score = 0
    test.attention = 0
    test.fluency= 0 
    test.language= 0
    test.memory= 0
    test.visuospatial= 0
    db.session.commit()
    questions= Module_1.query.filter_by(id= id).first()
    questions.question_1 = False
    questions.question_2 = False
    questions.question_3 = False
    questions.question_4 = False
    questions.question_5 = False
    questions.question_6 = False
    questions.question_7 = False
    questions.question_8 = False
    questions.question_9 = False
    questions.question_10 = False
    db.session.commit()
    day = None
    date= None
    month= None
    year= None
    season= None
    message= None
    next= None
    form = Fluency_1()
    if form.validate_on_submit():
        user = current_user
        id= user.id
        test= Test.query.filter_by(id= id).first()
        questions= Module_1.query.filter_by(id= id).first()
        print(test.attention)
        module_score= test.module_1_score
        attention= test.attention
        day = form.day.data
        date= form.date.data
        month= form.month.data
        year= form.year.data
        season= form.season.data
        actual_date= dt.today()
        actual_day= actual_date.day
        actual_year= actual_date.year
        day_now= calendar.day_name[actual_date.weekday()]
        month_now = str(calendar.month_name[actual_date.month])
        winter= ["December", "January", "February"]
        spring= ["March", "April", "May"]
        summer= ["June", "July", "August"]
        autumn= ["September", "October", "November"]
        season_now= " "
        print(month_now)
        if month_now in winter:
            season_now = "Winter"
        elif month_now in spring:
            season_now ="Spring"
        elif month_now in summer:
            season_now ="Summer"
        elif month_now in autumn:
            season_now ="Autumn"
        print(season)
        print(season_now)
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
        if season == season_now:
            print("season is correct")
            attention += 1
            module_score +=1
        test.attention= attention
        test.module_1_score= module_score
        questions.question_1= True
        db.session.commit()
        message= "Your answers have been accepted, please click next to continue"
        next= True
        return render_template("/modules/module1/fluency1.html", day= day, date= date, year= year, season= season,form=form,message= message, next= next)
        # except:
        #     message= "Sorry there was a problem, please try again"
        #     next= None
        #     return render_template("/modules/module1/fluency1.html", day= day, date= date, year= year, season= season,form=form,next=next,message= message)
    return render_template("/modules/module1/fluency1.html", day= day, date= date, year= year, season= season,form=form,next=next,message= message)

@app.route('/fluency2',methods=["GET", "POST"])
@login_required
def fluency2():
    user= current_user 
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    questions.question_2= True
    db.session.commit()
    return render_template("/modules/module1/fluency2.html")


@app.route('/fluency3',methods=["GET", "POST"])
@login_required
def fluency3():
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
        test= Test.query.filter_by(id= id).first()
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
        test.attention= attention
        test.module_1_score= module_score
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
    user= current_user
    id= user.id
    questions= Module_1.query.filter_by(id= id).first()
    questions.question_4=True
    db.session.commit()
    return render_template("/modules/module1/fluency4.html")

@app.route('/fluency5',methods=["GET", "POST"])
@login_required
def fluency5():
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
        test= Test.query.filter_by(id= id).first()
        questions= Module_1.query.filter_by(id= id).first()
        module_score= test.module_1_score
        memory= test.memory
        value_1 = form.v1.data.strip(" ")
        value_2 = form.v2.data.strip(" ")
        value_3 = form.v3.data.strip(" ")
        value_4 = form.v4.data.strip(" ")
        q1_answers=["johnson", "boris johnson"]
        q2_answers=["thatcher","margaret thatcher"]
        q3_answers=["biden","joe biden","joseph biden","jo biden"]
        q4_answers=["kennedy","john kennedy","john f. kennedy","john f kennedy"]
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
    questions.question_6=True
    db.session.commit()
    return render_template("/modules/module1/fluency6.html")

@app.route('/fluency7',methods=["GET", "POST"])
@login_required
def fluency7():
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
        test= Test.query.filter_by(id= id).first()
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
        q3_answers=["kangaroo","wallaby"]
        q4_answers=["penguin"]
        q5_answers=["anchor"]
        q6_answers=["camel","dromedary"]
        q7_answers=["harp"]
        q8_answers=["rhino","rhinoceros"]
        q9_answers=["barrel","keg","tub"]
        q10_answers=["crown"]
        q11_answers=["crocodile","alligator"]
        q12_answers=[" piano accordion","accordian","squeeze box"]
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
        test= Test.query.filter_by(id= id).first()
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
        test= Test.query.filter_by(id= id).first()
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


if __name__ == '__main__':
    app.run(port=80, debug=True)
   

    