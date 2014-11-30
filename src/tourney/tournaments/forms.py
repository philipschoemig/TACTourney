'''
Created on 22.10.2014

@author: Philip
'''

import flask_wtf
import wtforms
from wtforms.validators import InputRequired, Length, Optional


class TournamentForm(flask_wtf.Form):
    name = wtforms.StringField('Name', validators=[InputRequired(), Length(0, 128)])
    description = wtforms.TextAreaField('Description', validators=[Optional()])
    submit = wtforms.SubmitField('Save')


class PlayerForm(flask_wtf.Form):
    name = wtforms.StringField('Name', validators=[InputRequired()])
    submit = wtforms.SubmitField('Save')
