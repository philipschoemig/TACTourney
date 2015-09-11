'''
Created on 22.08.2015

@author: Philip Schoemig
'''
import unittest

from data import db
from app import app
import users.views


class TestViews(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            users.models.User.create(username='admin',
                                     password='default',
                                     role_enum=users.constants.Roles.admin)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def register(self, username, email, password):
        return self.client.post('/users/register', data=dict(
            username=username,
            email=email,
            password=password,
            password2=password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.client.post('/users/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/users/logout', follow_redirects=True)

    def test_login(self):
        rv = self.login('admin', 'default')
        self.assertIn('You have been logged in', rv.data)
        rv = self.logout()
        self.assertIn('You have been logged out', rv.data)
        rv = self.login('adminx', 'default')
        self.assertIn('Invalid username or password', rv.data)
        rv = self.login('admin', 'defaultx')
        self.assertIn('Invalid username or password', rv.data)

    def test_logout(self):
        rv = self.logout()
        self.assertIn('You have been logged out', rv.data)

    def test_register(self):
        rv = self.register('user', 'user@test.com', 'default')
        self.assertIn('Your account has been created', rv.data)
