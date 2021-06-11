from app import Users 
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['DEBUG'] = True

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:F41r4cr3/P1pps@localhost/themindgarden'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db = SQLAlchemy(app)

password= 'Th3m1ndg4rd3n2421!'
password_hashed= generate_password_hash(password)
admin_user=Users(first_name='admin',last_name='admin', dob='24-01-1991',email_address='themindgarden21@gmail.com',password_hash=password_hashed, admin=True )
db.session.add(admin_user)
db.session.commit()