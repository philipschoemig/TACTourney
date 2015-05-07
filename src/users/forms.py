'''
Created on 22.10.2014

@author: Philip
'''

import flask_wtf
import wtforms
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional

import users.models


class UserForm(flask_wtf.Form):
    username = wtforms.StringField(
        'Username', validators=[InputRequired(), Length(0, 64)])
    email = wtforms.StringField(
        'Email address', validators=[InputRequired(), Email(), Length(0, 256)])
    full_name = wtforms.StringField(
        'Full name', validators=[Optional(), Length(0, 256)])
    password = wtforms.PasswordField(
        'Password', validators=[EqualTo('password2',
                                        message='Passwords must match.')])
    password2 = wtforms.PasswordField('Confirm Password')
    role = wtforms.SelectField('Role', coerce=int)
    submit = wtforms.SubmitField('Save')

    def validate_username(self, field):
        # Check if username field was changed
        if field.data != field.default:
            # Check if the data matches an existing username
            if users.models.User.query.filter_by(username=field.data).first():
                raise wtforms.ValidationError('Username already in use.')


class RegisterForm(UserForm):
    password = wtforms.PasswordField(
        'Password', validators=[InputRequired(),
                                EqualTo('password2',
                                        message='Passwords must match.')])
    password2 = wtforms.PasswordField(
        'Confirm Password', validators=[InputRequired()])
    role = None
    recaptcha = flask_wtf.RecaptchaField()
    submit = wtforms.SubmitField('Register')


class LoginForm(flask_wtf.Form):
    username = wtforms.StringField(
        'Username', validators=[InputRequired(), Length(0, 64)])
    password = wtforms.PasswordField('Password', validators=[InputRequired()])
    submit = wtforms.SubmitField('Log In')
