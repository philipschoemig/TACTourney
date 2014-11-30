'''
Created on 22.10.2014

@author: Philip
'''

import flask_wtf
import wtforms


class ConfirmationForm(flask_wtf.Form):
    radio = wtforms.RadioField(choices=[('yes', 'Yes'), ('no', 'No')],
                               default='no',
                               validators=[wtforms.validators.InputRequired()])
    submit = wtforms.SubmitField('Confirm')
