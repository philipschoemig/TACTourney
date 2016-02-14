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

    def test_table(self):
        self.login('admin', 'default')
        rv = self.client.get('/users/table')
        self.assertIn('admin', rv.data)

    def test_add(self):
        self.login('admin', 'default')
        rv = self.client.post('/users/add', data=dict(
            username='user',
            email='user@test.com',
            full_name='Test user',
            password='default',
            password2='default',
            role=0
        ), follow_redirects=True)
        self.assertIn('The user has been saved', rv.data)

    def test_edit(self):
        self.login('admin', 'default')
        rv = self.client.get('/users/edit/2', follow_redirects=True)
        self.assertIn('Not found: User ID 2', rv.data)

        rv = self.client.post('/users/add', data=dict(
            username='user',
            email='user@test.com',
            full_name='Test user',
            password='default',
            password2='default',
            role=0
        ), follow_redirects=True)

        rv = self.client.post('/users/edit/2', data=dict(
            username='user',
            email='user@mytest.com',
            full_name='Test user',
            password='default',
            password2='default',
            role=0
        ), follow_redirects=True)
        self.assertIn('The user has been saved', rv.data)
        self.assertIn('user@mytest.com', rv.data)

    def test_delete(self):
        self.login('admin', 'default')
        rv = self.client.get('/users/delete/2', follow_redirects=True)
        self.assertIn('Not found: User ID 2', rv.data)

        rv = self.client.post('/users/add', data=dict(
            username='user',
            email='user@test.com',
            full_name='Test user',
            password='default',
            password2='default',
            role=0
        ), follow_redirects=True)

        rv = self.client.get('/users/delete/2', follow_redirects=True)
        self.assertIn('Do you really want to delete this user?', rv.data)

        # rv = self.client.post('/users/delete/2', data=dict(
        #     radio='radio-0'
        # ), follow_redirects=True)
        # self.assertIn('Do you really want to delete this user?t', rv.data)


if __name__ == '__main__':
    unittest.main()
