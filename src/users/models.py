'''
Created on 22.10.2014

@author: Philip
'''

import flask_login
import werkzeug.security

from data import db
import users.constants
import utils.models


team_user = db.Table('team_user',
                     db.Column(
                         'team_id', db.Integer, db.ForeignKey('team.id')),
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                     )
tournament_user = db.Table('tournament_user',
                     db.Column(
                         'tournament_id', db.Integer, db.ForeignKey('tournament.id')),
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(db.Model, flask_login.UserMixin, utils.models.CRUDMixin):

    '''
    classdocs
    '''
    id = db.Column(db.Integer, primary_key=True, info={'label': 'ID'})
    username = db.Column(
        db.String(64), unique=True, info={'label': 'Username'})
    email = db.Column(
        db.String(256), unique=False, info={'label': 'Email address'})
    full_name = db.Column(
        db.String(256), unique=False, info={'label': 'Full name'})
    password_hash = db.Column(db.String(128), unique=False)
    role = db.Column(db.SmallInteger,
                     default=users.constants.Roles.player.index,
                     info={'label': 'Role', 'attr': 'role_string'})

    tournaments = db.relationship('tournaments.models.Tournament',
                                  secondary=tournament_user,
                                  backref='users',
                                  lazy='dynamic')
    teams = db.relationship('teams.models.Team',
                            secondary=team_user,
                            backref='users',
                            lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        if len(password) > 0:
            self.password_hash = werkzeug.security.generate_password_hash(
                password)

    def verify_password(self, password):
        return werkzeug.security.check_password_hash(self.password_hash, password)

    @property
    def role_enum(self):
        return users.constants.Roles[self.role]

    @role_enum.setter
    def role_enum(self, role):
        self.role = role.index

    @property
    def role_string(self):
        return str(self.role_enum).capitalize()

    def is_admin(self):
        return self.role_enum == users.constants.Roles.admin

    def is_manager(self):
        return self.role_enum == users.constants.Roles.manager or self.is_admin()

    def is_readable(self, user):
        return True

    def is_writeable(self, user):
        if user != self and not user.is_admin():
            return False
        return True

    def has_access(self, user):
        if user != self and not user.is_admin():
            return False
        return True

    def __repr__(self):
        return '<User %r>' % self.username
