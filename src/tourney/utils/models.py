'''
Created on 22.10.2014

@author: Philip
'''

from data import db
import users.constants


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, commit=True, form=None, **kwargs):
        instance = cls(**kwargs)
        if form:
            form.populate_obj(instance)
        return instance.save(commit)

    @classmethod
    def get(cls, identifier):
        return cls.query.get(identifier)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, identifier):
        return cls.query.get_or_404(identifier)

    def update(self, commit=True, form=None, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        if form:
            form.populate_obj(self)
        return commit and db.session.commit()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class UserAccessMixin(object):
    def has_access(self, user):
        return self.user.has_access(user)

    @classmethod
    def filter_user(cls, user):
        query = cls.query
        if not user.is_admin():
            query = query.filter_by(user=user)
        return query
