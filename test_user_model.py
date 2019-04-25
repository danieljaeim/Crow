"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, User, Message, Follows, connect_db
from sqlalchemy.exc import IntegrityError
from psycopg2 import IntegrityError as IError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database
from app import app

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler-test'


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data



class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.create_all()

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=''
        )

        u2 = User.signup(
            email="test1@test.com",
            username="test2user",
            password="HASHED_PASSWORD",
            image_url=''
        )



        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        
        newFollow=Follows(user_being_followed_id=2, user_following_id=1)
        
        db.session.add(newFollow)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        
        db.session.close()
        db.drop_all(bind=None)

    def test_user_model(self):
        """Does basic model work?"""

        u = User.query.get_or_404(1)
        u2 = User.query.get_or_404(2)

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(u2.is_followed_by(u), True)
        self.assertEqual(u.is_following(u2), True)
        self.assertEqual(u.__repr__(), f"<User #1: testuser, test@test.com>")
        self.assertEqual(User.authenticate(username="test2user", password="HASHED_PASSWORD"), User.query.filter_by(username="test2user").first())
        self.assertEqual(User.authenticate(username="fakeuser", password="HASHED_PASSWORD"),False)
        self.assertEqual(User.authenticate(username="test2user", password="FakePW"),False)
        # self.assertEqual(User.signup(username='user3', email='test@email.com', password='hashed_pwd', image_url=""), User.query.get(3))
        
        # def user_signup():
        #     try: 
        #         user3 = User.signup(username='user4', email='test1@test.com', password='hashed_pwd', image_url="")
        #     except IError as err:
        #         return err
        #     else:
        #         return IntegrityError

        # self.assertEqual(user_signup(), IntegrityError)


        
        


