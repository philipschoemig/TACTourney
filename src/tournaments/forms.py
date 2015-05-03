'''
Created on 22.10.2014

@author: Philip
'''

import flask_login
import flask_wtf
import wtforms
from wtforms.validators import InputRequired, Length, Optional
import wtforms_alchemy  # Required for wtforms.ext.sqlalchemy

import users.models


class TournamentForm(flask_wtf.Form):
    name = wtforms.StringField('Name', validators=[InputRequired(), Length(0, 128)])
    description = wtforms.TextAreaField('Description', validators=[Optional()])
    users = wtforms.ext.sqlalchemy.fields.QuerySelectMultipleField(
        label='Organizers',
        query_factory=lambda: users.models.User.query.filter(users.models.User.role < 2),
        get_pk=lambda item: item.id,
        get_label=lambda item: item.username,
        default=lambda: [flask_login.current_user],
        validators=[wtforms.validators.InputRequired()])
    submit = wtforms.SubmitField('Save')

    def validate_users(self, field):
        # Check if the maximum number of tournament organizers is exceeded
        if len(field.data) > 3:
            raise wtforms.ValidationError('A tournament may only have up to three organizers')
