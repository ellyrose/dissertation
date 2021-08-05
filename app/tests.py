from datetime import date
import unittest
import os
import sys
from datetime import date
from urllib.parse import urlparse


topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from app import  app, db, Users, Test

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


    def test_fluency1_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 10 and test.attention == 10)

    def test_fluency1_day_plus2(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='6',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 10 and test.attention == 10)

    def test_fluency1_day_minus2(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='2',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 10 and test.attention == 10)

    def test_fluency1_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        response = self.app.get('/fluency1')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency1_navigate_forward(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        response = self.app.get('/fluency3')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')
       

    def test_fluency2_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 13 and test.attention == 13)

    def test_fluency2_different_order(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="key",v2="ball",v3="lemon"))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 13 and test.attention == 13)

    def test_fluency2_repeat_answer(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="lemon",v3="ball"))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 12 and test.attention == 12)

    def test_fluency2_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        response = self.app.get('/fluency1')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency2_navigate_forward(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        response = self.app.get('/fluency4')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')


    def test_fluency3_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 18 and test.attention == 18)

    def test_fluency3_correct_with_space(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1='93 ',v2='86 ',v3='79 ',v4='72' ,v5='65 '))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 18 and test.attention == 18)


    def test_fluency3_0_answer(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        response= self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=0))
        self.assertTrue("You must enter the number in digits" in response.get_data(as_text=True))

    def test_fluency3_non_int_answer(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        response =self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5='sixty-five'))
        self.assertTrue("You must enter the number in digits" in response.get_data(as_text=True))

    

    def test_fluency3_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        response = self.app.get('/fluency2')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency3_navigate_forward(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        response = self.app.get('/fluency5')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency4_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="lemon",v2="key",v3="ball"))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 21 and test.attention == 18 and test.memory == 3)

    def test_fluency4_different_order(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 21 and test.attention == 18 and test.memory == 3)

    def test_fluency4_repeat_answer(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="lemon",v2="lemon",v3="ball"))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 20 and test.attention == 18 and test.memory == 2)

    def test_fluency4_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="lemon",v2="key",v3="ball"))
        response = self.app.get('/fluency3')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency4_navigate_forward(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="lemon",v2="key",v3="ball"))
        response = self.app.get('/fluency6')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')
        
    def test_fluency5_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 25 and test.attention == 18 and test.memory == 7)

    def test_fluency5_capital(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='BORRIS JOHNSON',v2='Margaret Thatcher',v3='JOe BIden',v4='JOHN kennedy'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 25 and test.attention == 18 and test.memory == 7)


    def test_fluency5_space(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson ',v2='margaret thatcher ',v3='joe biden ',v4='john kennedy '))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 25 and test.attention == 18 and test.memory == 7)

    def test_fluency5_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson ',v2='margaret thatcher ',v3='joe biden ',v4='john kennedy '))
        response= self.app.get('/fluency4')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency5_navigate_forward(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson ',v2='margaret thatcher ',v3='joe biden ',v4='john kennedy '))
        response= self.app.get('/fluency7')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency7_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 41 and test.attention == 18 and test.memory == 7 and test.language ==16)

    def test_fluency7_correct_capital(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='SPOON',v2='boOK',v3='Kangaroo',v4='PENGUIN', v5='ANCHor',v6='CAmel',v7='HARP',v8='RHino',v9='BARREL',v10='CROWN',
        v11='crocoDILe',v12='Accordian'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 41 and test.attention == 18 and test.memory == 7 and test.language ==16)

    def test_fluency7_correct_space(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon ',v2='book ',v3='kangaroo ',v4='penguin ', v5='anchor ',v6='camel ',v7='harp ',v8='rhino ',v9='barrel ',v10='crown ',
        v11='crocodile ',v12='accordian '))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 41 and test.attention == 18 and test.memory == 7 and test.language ==16)      

    def test_fluency7_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        response= self.app.get('/fluency6')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency7_navigate_forward(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        response= self.app.get('/fluency9')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency8_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 45 and test.attention == 18 and test.memory == 7 and test.language ==20)  

    def test_fluency8_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        response= self.app.get('/fluency7')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')

    def test_fluency8_navigate_forward(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        response= self.app.get('/fluency10')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')


    def test_fluency9_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        self.app.post(
        '/fluency9',
        data=dict(v1=8,v2=10,v3=7,v4=9))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 49 and test.attention == 18 and test.memory == 7 and test.language ==20, test.visuospatial== 4)  
   
   
    def test_fluency9_correct_with_space(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        self.app.post(
        '/fluency9',
        data=dict(v1='8 ',v2='10 ',v3='7 ',v4='9 '))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 49 and test.attention == 18 and test.memory == 7 and test.language ==20, test.visuospatial== 4)
  
    def test_fluency9_0_answer(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        response =self.app.post(
        '/fluency9',
        data=dict(v1=0,v2=10,v3=7,v4=9))
        self.assertTrue("You must enter the number in digits" in response.get_data(as_text=True))

    def test_fluency9_non_int_answer(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        response =self.app.post(
        '/fluency9',
        data=dict(v1='ten',v2=10,v3=7,v4=9))
        self.assertTrue("You must enter the number in digits" in response.get_data(as_text=True))

        
    def test_fluency9_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        self.app.post(
        '/fluency9',
        data=dict(v1=10,v2=10,v3=7,v4=9))
        response = self.app.get('/fluency8')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')



    def test_fluency10_correct(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        self.app.post(
        '/fluency9',
        data=dict(v1=8,v2=10,v3=7,v4=9))
        self.app.post(
        '/fluency10',
        data=dict(v1='k',v2='m',v3='a',v4='t'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 53 and test.attention == 18 and test.memory == 7 and test.language ==20, test.visuospatial== 6)  
   
        
    def test_fluency10_correct_space(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        self.app.post(
        '/fluency9',
        data=dict(v1=8,v2=10,v3=7,v4=9))
        self.app.post(
        '/fluency10',
        data=dict(v1='k ',v2='m ',v3='a ',v4='t '))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 53 and test.attention == 18 and test.memory == 7 and test.language ==20, test.visuospatial== 6) 


    def test_fluency10_correct_capital(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        self.app.post(
        '/fluency9',
        data=dict(v1=8,v2=10,v3=7,v4=9))
        self.app.post(
        '/fluency10',
        data=dict(v1='K',v2='M',v3='A',v4='T'))
        id = user.id
        test= Test.query.filter_by(userid= id, completed= False).first()
        self.assertTrue(test.module_1_score == 53 and test.attention == 18 and test.memory == 7 and test.language ==20, test.visuospatial== 6)


    def test_fluency10_navigate_back(self):
        user = Users( first_name='Elly',last_name='Turnbull',dob=date.today(),email_address='test@test.com', 
        country="United Kingdom",password_hash="pppppppppppp")
        user.password= 'pppppppppppp'
        db.session.add(user)
        db.session.commit()
        self.login('test@test.com',"pppppppppppp")
        self.app.post(
        '/fluency1',
        data=dict(day='Wednesday',date='4',month='August',year='2021',season='Summer', birthdate=date.today(), email_address='test@test.com', 
        test_place='Fluency Fountain',age='0',country='United Kingdom'))
        self.app.post(
        '/fluency2',
        data=dict(v1="lemon",v2="key",v3="ball"))
        self.app.post(
        '/fluency3',
        data=dict(v1=93,v2=86,v3=79,v4=72,v5=65))
        self.app.post(
        '/fluency4',
        data=dict(v1="ball",v2="lemon",v3="key"))
        self.app.post(
        '/fluency5',
        data=dict(v1='borris johnson',v2='margaret thatcher',v3='joe biden',v4='john kennedy'))
        self.app.post(
        '/fluency6',
        data=dict(v1=1,v2=1,v3=1,v4=1))
        self.app.post(
        '/fluency7',
        data=dict(v1='spoon',v2='book',v3='kangaroo',v4='penguin', v5='anchor',v6='camel',v7='harp',v8='rhino',v9='barrel',v10='crown',
        v11='crocodile',v12='accordian'))
        self.app.post(
        '/fluency8',
        data=dict(v1=10,v2=3,v3=4,v4=5))
        self.app.post(
        '/fluency9',
        data=dict(v1=8,v2=10,v3=7,v4=9))
        self.app.post(
        '/fluency10',
        data=dict(v1='K',v2='M',v3='A',v4='T'))
        response= self.app.get('/fluency9')
        self.assertEqual(urlparse(response.location).path, '/yourgarden')


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