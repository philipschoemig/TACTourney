'''
Created on 22.10.2014

@author: Philip
'''

import flask
import flask_login

import users.forms
import users.models
import utils.forms
import utils.redirect
from utils.views import alert_warning, alert_info, alert_success, \
    error_not_found, error_access_denied, create_action_urls


bp_users = flask.Blueprint("users", __name__)

@bp_users.route('/login', methods=['GET', 'POST'])
def login():
    form = users.forms.LoginForm()
    if form.validate_on_submit():
        user = users.models.User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            flask_login.login_user(user, True)
            return utils.redirect.redirect_back('index')
            #return flask.redirect(flask.url_for('index'))
        alert_warning('Invalid username or password')
    return flask.render_template('login.html', form=form)


@bp_users.route('/logout')
def logout():
    flask_login.logout_user()
    alert_info('You have been logged out')
    return flask.redirect(flask.url_for('.login'))


@bp_users.route('/register', methods=['GET', 'POST'])
def register():
    form = users.forms.RegisterForm()
    if form.validate_on_submit():
        users.models.User.create(form=form)
        alert_success('Your account has been created')
        return flask.redirect(flask.url_for('.login'))
    return flask.render_template('register.html', form=form)


@bp_users.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@flask_login.login_required
def edit_user(user_id):
    user = users.models.User.query.filter_by(id=user_id).first()
    if user is None:
        return error_not_found('User ID {}'.format(user_id), 'index')
    if user != flask_login.current_user and user.role != users.constants.Roles.admin:
        return error_access_denied('User ID {}'.format(user_id), 'index')
    
    form = users.forms.UserForm(flask.request.form, user)
    if form.validate_on_submit():
        user.update(form=form)
        alert_success('Your account has been saved')
    
    actions = create_action_urls({'Delete': '.delete_user'}, user, user_id='id')
    return flask.render_template('edit_page.html', type="User", name=user.username, form=form, actions=actions)


@bp_users.route('/users/delete/<int:user_id>', methods=['GET', 'POST'])
@flask_login.login_required
def delete_user(user_id):
    user = users.models.User.query.filter_by(id=user_id).first()
    if user is None:
        return error_not_found('User ID {}'.format(user_id), 'index')
    if user != flask_login.current_user and user.role != users.models.Role.ADMIN:
        return error_access_denied('User ID {}'.format(user_id), 'index')
    
    form = utils.forms.ConfirmationForm()
    if form.validate_on_submit():
        if form.radio.data == 'yes':
            user.delete()
            alert_success('The user has been deleted')
        return flask.redirect(flask.url_for('index'))
    
    return flask.render_template('delete_page.html', type="User", name=user.username, form=form)
