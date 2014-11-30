'''
Created on 22.10.2014

@author: Philip
'''

import flask_login
import werkzeug.security

from data import db
import users.constants
import utils.models


class User(db.Model, flask_login.UserMixin, utils.models.CRUDMixin):
    '''
    classdocs
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, info={'label': 'Username'})
    email = db.Column(db.String(256), unique=False, info={'label': 'E-Mail'})
    full_name = db.Column(db.String(256), unique=False, info={'label': 'Full name'})
    password_hash = db.Column(db.String(128), unique=False)
    role_enum = db.Column(db.SmallInteger, default=users.constants.Roles.player.index, info={'label': 'Role'})
    
    tournaments = db.relationship('tournaments.models.Tournament', backref='user', lazy='dynamic')
    teams = db.relationship('teams.models.Team', backref='user', lazy='dynamic')
#     player = db.relationship('Player', backref='user', lazy='dynamic')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = werkzeug.security.generate_password_hash(password)
    
    @property
    def role(self):
        return users.constants.Roles[self.role_enum]
    
    @role.setter
    def role(self, role):
        self.role_enum = role.index
    
    def verify_password(self, password):
        return werkzeug.security.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User %r>' % self.username
