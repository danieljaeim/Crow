from unittest import TestCase
import unittest
from models import db, User, Message, Follows, connect_db
from sqlalchemy.exc import IntegrityError
import forms
from psycopg2 import IntegrityError as IError
import os

from app import app, CURR_USER_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler-test'
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


class UserViews(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        db.create_all()


        self.client = app.test_client()

        self.user1 = User(
            email='test@test.com', username='user1', image_url="", header_image_url="", bio="This is my bio", location="Denver", password="HASHED_PASSWORD")

        self.user2 = User(
            email='test2@test.com', username='user2', image_url="", header_image_url="", bio="This is my bio", location="Denver", password="HASHED_PASSWORD")

        self.user3 = User(
            email='test3@test.com', username='user3', image_url="", header_image_url="", bio="This is my bio", location="Denver", password="HASHED_PASSWORD")

        for user in [self.user1, self.user2, self.user3]:
            db.session.add(user)
            db.session.commit()

    def tearDown(self):

        db.session.close()
        db.drop_all(bind=None)

    def test_user_views(self):

        self.assertEqual(User.query.get(1), self.user1)

    def test_logged_in_view_follower_page(self):

        self.client = app.test_client()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

        response = self.client.get(f'/users/{self.user1.id}/following')
        response2 = self.client.get(f'/users/{self.user1.id}/followers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_logged_out_view_follower_page(self):

        self.client = app.test_client()

        response = self.client.get(f'/users/{self.user1.id}/following')
        response2 = self.client.get(f'/users/{self.user1.id}/followers')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    def test_logged_in_message_page(self):


        redirect = ('http://localhost/users/1')

        self.client = app.test_client()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

        #first message with id = 1
        response = self.client.post(
            '/messages/new', data={'text': 'Sample text'})


        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.query.get(1).text, 'Sample text')
        self.assertEqual(Message.query.get(1).user.id, self.user1.id)
        

        new_message=Message(text='empty string', timestamp="2016-03-10", user_id=2)
        db.session.add(new_message)
        db.session.commit()

        response = self.client.post(
            '/messages/1/delete', )
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Message.query.filter(id == self.user1.id).all(), [])  


        response = self.client.post(
            '/messages/2/delete', )
        self.assertEqual(response.data, b'"Go and kiss your mother\'s behind"\n')  
        self.assertEqual(Message.query.filter(id != self.user1.id).all(), [Message.query.get(2)])  

    def test_logged_out_message_page(self):

        response = self.client.post(
            '/messages/new', data={'text': 'Sample text'})

        redirect = ('http://localhost/')

        self.assertEqual(response.location, redirect)
        self.assertEqual(Message.query.all(), [])  

        response = self.client.post(
            '/messages/1/delete')
        self.assertEquals(response.status_code, 302)  
        self.assertEquals(Message.query.all(), [])  

        self.assertEqual(response.location, redirect)

      


    # def test_submitted_and_valid(self):
    #     with self.request(method='POST', data={'name':'foo'}):
    #         f = FooForm(request.form, csrf_enabled=False)
    #         self.assertEqual(f.validate_on_submit(), True)


    
