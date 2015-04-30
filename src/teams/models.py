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
                        info={'label': 'Members', 'attr': 'users_string'})
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))

    @property
    def users_string(self):
        return ", ".join([user.username for user in self.users])

    def has_access(self, user):
        for u in self.users:
            if u.has_access(user):
                return True
        return False

    @classmethod
    def filter_user(cls, user):
        query = cls.query
        if not user.is_admin():
            query = query.filter(cls.users.contains(user))
        return query

    def __repr__(self):
        return '<Team %r>' % self.name
