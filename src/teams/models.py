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
    id = db.Column(db.Integer, primary_key=True, info={'label': 'ID'})
    name = db.Column(db.String(128), unique=True, info={'label': 'Name'})

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        info={'label': 'Players', 'attr': 'users_string'})
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))

    @property
    def users_string(self):
        return ", ".join([user.username for user in self.users])

    def __repr__(self):
        return '<Team %r>' % self.name
