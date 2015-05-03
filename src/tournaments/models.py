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

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        info={'label': 'Organizers', 'attr': 'users_string'})

    teams = db.relationship(
        'teams.models.Team', backref='tournament', lazy='dynamic')

    @property
    def users_string(self):
        return ", ".join([user.username for user in self.users])

    def __repr__(self):
        return '<Tournament %r>' % self.name
