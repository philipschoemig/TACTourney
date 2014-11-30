'''
Created on 22.10.2014

@author: Philip
'''

import flask_wtf
import wtforms


class TeamForm(flask_wtf.Form):
    name = wtforms.StringField('Name',
                               validators=[wtforms.validators.InputRequired(), wtforms.validators.Length(0, 128)])
    submit = wtforms.SubmitField('Save')
