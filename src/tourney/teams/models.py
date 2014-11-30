'''
Created on 22.10.2014

@author: Philip
'''

from data import db
import utils.models


class Team(db.Model, utils.models.UserAccessMixin, utils.models.CRUDMixin):
    '''
    classdocs
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, info={'label': 'Name'})

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), info={'label': 'Owner', 'attr': 'user.username'})
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    
#     players = db.relationship('Player', backref='team', lazy='dynamic')
    
    def __repr__(self):
        return '<Team %r>' % self.name
