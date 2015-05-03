'''
Created on 22.10.2014

@author: Philip
'''

import difflib

import flask_login
import flask_wtf
import wtforms
import wtforms_alchemy  # Required for wtforms.ext.sqlalchemy

import teams.models
import users.models


class TeamForm(flask_wtf.Form):
    name = wtforms.StringField('Name',
                               validators=[wtforms.validators.InputRequired(),
                                           wtforms.validators.Length(0, 128)])
    users = wtforms.ext.sqlalchemy.fields.QuerySelectMultipleField(
        label='Players',
        query_factory=lambda: users.models.User.query,
        get_pk=lambda item: item.id,
        get_label=lambda item: item.username,
        default=lambda: [flask_login.current_user],
        validators=[wtforms.validators.InputRequired()])
    submit = wtforms.SubmitField('Save')

    def validate_name(self, field):
        # Check if name field was changed
        if field.data != field.default:
            # Retrieve list of all team names
            query = teams.models.Team.query.with_entities(
                teams.models.Team.name).all()
            names = [name[0] for name in query]
            # Check if the data matches an existing team name
            result = difflib.get_close_matches(field.data, names, 1)
            if len(result) > 0:
                raise wtforms.ValidationError(
                    'Similar name already in use: ' + result[0])

    def validate_users(self, field):
        # Check if the maximum number of team players is exceeded
        if len(field.data) > 2:
            raise wtforms.ValidationError('A team may only have up to two players')
