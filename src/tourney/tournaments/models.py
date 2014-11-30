'''
Created on 22.10.2014

@author: Philip
'''

from data import db
import utils.models


class Tournament(db.Model, utils.models.UserAccessMixin, utils.models.CRUDMixin):
    '''
    classdocs
    '''
    id = db.Column(db.Integer, primary_key=True, info={'label': 'ID'})
    name = db.Column(db.String(128), unique=False, info={'label': 'Name'})
    description = db.Column(db.Text(), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), info={'label': 'Owner', 'attr': 'user.username'})
    
    teams = db.relationship('teams.models.Team', backref='tournament', lazy='dynamic')
    
    def __repr__(self):
        return '<Tournament %r>' % self.name


# class Player(db.Model, utils.models.CRUDMixin):
#     '''
#     classdocs
#     '''
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), unique=False)
#     email = db.Column(db.String(255), unique=False)
#     phone = db.Column(db.String(255), unique=False)
# 
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
#     
#     def __repr__(self):
#         return '<Player %r>' % self.name
