'''
Created on 09.05.2015

@author: Philip Schoemig
'''

import os
import unittest

from data import db
from app import app
import users.models


class TestModels(unittest.TestCase):

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

    def test_password_getter(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            with self.assertRaisesRegexp(AttributeError, "password is not a readable attribute"):
                user.password

    def test_password_setter(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            user.password = 'test'
            result = user.verify_password('test')
            self.assertTrue(result)

    def test_verify_password(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            result = user.verify_password('default')
            self.assertTrue(result)

    def test_role_enum_getter(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            self.assertEqual(users.constants.Roles.admin, user.role_enum)

    def test_role_enum_setter(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            user.role_enum = users.constants.Roles.manager
            self.assertEqual(users.constants.Roles.manager, user.role_enum)

    def test_role_string_getter(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            self.assertEqual('Admin', user.role_string)

    def test_role_string_setter(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            with self.assertRaisesRegexp(AttributeError, "can't set attribute"):
                user.role_string = 'Manager'

    def test_is_admin(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            self.assertTrue(user.is_admin)

    def test_is_manager(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            self.assertTrue(user.is_manager)

    def test_is_readable(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            self.assertTrue(user.is_readable)

    def test_is_writeable(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            self.assertTrue(user.is_writeable)

    def test_has_access(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            self.assertTrue(user.has_access)

    def test_str(self):
        with self.client.session_transaction():
            user = users.models.User.query.filter_by(username='admin').first()
            self.assertEqual("<User u'admin'>", str(user))
