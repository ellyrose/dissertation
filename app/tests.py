from datetime import date
import unittest
import os
import sys
from datetime import date
from flask import url_for


topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from app import app, db, Users, Test

class FunctionalityTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_account(self, first_name, last_name, birthdate, email_address,country, password_hash,confirm,accept_tos):
        return self.app.post(
        '/createaccount',
        data=dict(first_name = first_name,last_name=last_name, birthdate=birthdate, email_address=email_address, 
        country=country, password_hash=password_hash, confirm=confirm, accept_tos=accept_tos),
        follow_redirects=True
        ) 
       
 
    def login(self, email_address, password_hash):
            return self.app.post(
            '/login',
            data=dict(email_address=email_address, password_hash=password_hash),
            follow_redirects=True
            )
    
    def logout(self):
        return self.app.get(
        '/logout',
        follow_redirects=True
        )
    
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_account_creation(self):
        response = self.create_account( 'Elly','Turnbull',date.today(),'test@test.com', 
        "United Kingdom","pppppppppppp", "pppppppppppp", True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Your account was created successfully!" in response.get_data(as_text=True))

    def test_account_creation_short_password(self):
        response = self.create_account( 'Elly','Turnbull',date.today(),'test@test.com', 
        "United Kingdom","pppp", "pppp", True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Your password must contain at least 12 characters, and at most 30 characters" in response.get_data(as_text=True))
     
    def test_account_creation_long_password(self):
        response = self.create_account( 'Elly','Turnbull',date.today(),'test@test.com', 
        "United Kingdom","pppppppppppppppppppppppppppppppp", "pppppppppppppppppppppppppppppppp", True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Your password must contain at least 12 characters, and at most 30 characters" in response.get_data(as_text=True))
    
    def test_account_creation_missmatched_passwords(self):
        response = self.create_account( 'Elly','Turnbull',date.today(),'test@test.com', 
        "United Kingdom","pppppppppppp", "pppppppp", True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("The two passwords must match" in response.get_data(as_text=True))
     
    def test_account_creation_email_in_use(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        db.session.add(user)
        db.session.commit()
        response = self.create_account( 'Elly','Turnbull',date.today(),'test@test.com', 
        "United Kingdom","pppppppppppp", "pppppppppppp", True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Sorry, please choose a different email address" in response.get_data(as_text=True))

    def test_login(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        response = self.login('test@test.com',"pppppppppppp")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Welcome to The Mind Garden, Elly</h1>" in response.get_data(as_text=True))

    def test_login_invalid_pw(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        response = self.login('test@test.com',"qqqqqqqqqqqq")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("You have entered an incorrect email address or password" in response.get_data(as_text=True))

    def test_login_invalid_email(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        response = self.login('elly@test.com',"pppppppppppp")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("You have entered an incorrect email address or password" in response.get_data(as_text=True))

    def test_logout(self):
            user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
            country="United Kingdom",password_hash="pppppppppppp")
            user.password= 'pppppppppppp'
            db.session.add(user)
            db.session.commit()
            self.login('test@test.com',"pppppppppppp")
            response = self.logout()
            self.assertEqual(response.status_code, 200)
            self.assertTrue("You have been logged out!</h1>" in response.get_data(as_text=True))


class FluencyTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_account(self, first_name, last_name, birthdate, email_address,country, password_hash,confirm,accept_tos):
        return self.app.post(
        '/createaccount',
        data=dict(first_name = first_name,last_name=last_name, birthdate=birthdate, email_address=email_address, 
        country=country, password_hash=password_hash, confirm=confirm, accept_tos=accept_tos),
        follow_redirects=True
        ) 
       
 
    def login(self, email_address, password_hash):
            return self.app.post(
            '/login',
            data=dict(email_address=email_address, password_hash=password_hash),
            follow_redirects=True
            )


    def test_fluency1(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Tuesday',date='27',month='July',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='fluency fountain',age='0',country='United Kingdom'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        print(test.module_1_score)
        self.assertTrue(test.module_1_score == 10)


        



          
  
class UserTests(unittest.TestCase):
    def test_password_setter(self):
        user = Users(password = 'password')
        self.assertTrue(user.password_hash is not None)

    def test_password_check(self):
        user = Users(password = 'password')
        self.assertTrue(user.verify_password('password'))
        self.assertFalse(user.verify_password('password1'))

    def test_password_salt_is_different(self):
        user = Users(password='password')
        user2 = Users(password='password')
        self.assertTrue(user.password_hash != user2.password_hash)



  

if __name__ == "__main__":
    unittest.main()