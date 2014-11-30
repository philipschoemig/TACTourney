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
from utils.views import get_column_names, create_table, alert_warning, alert_info, alert_success, \
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


@bp_users.route('/table')
@flask_login.login_required
def table():
    if not flask_login.current_user.is_admin():
        return error_access_denied('Users', 'index')
    models = users.models.User.query.all()
    columns = get_column_names(users.models.User())
    table = create_table(models, {'Edit': '.edit', 'Delete': '.delete'}, user_id='id')
    actions = None #create_action_urls({'Add': '.add'})
    return flask.render_template('table_page.html', type="Users", columns=columns, table=table, actions=actions)


@bp_users.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@flask_login.login_required
def edit(user_id):
    user = users.models.User.query.filter_by(id=user_id).first()
    if user is None:
        return error_not_found('User ID {}'.format(user_id), 'index')
    if not user.has_access(flask_login.current_user):
        return error_access_denied('User ID {}'.format(user_id), 'index')
    
    form = users.forms.UserForm(flask.request.form, user)
    if form.validate_on_submit():
        user.update(form=form)
        alert_success('Your account has been saved')
    
    actions = create_action_urls({'Delete': '.delete'}, user, user_id='id')
    return flask.render_template('edit_page.html', type="User", name=user.username, form=form, actions=actions)


@bp_users.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@flask_login.login_required
def delete(user_id):
    user = users.models.User.query.filter_by(id=user_id).first()
    if user is None:
        return error_not_found('User ID {}'.format(user_id), 'index')
    if not user.has_access(flask_login.current_user):
        return error_access_denied('User ID {}'.format(user_id), 'index')
    
    form = utils.forms.ConfirmationForm()
    if form.validate_on_submit():
        if form.radio.data == 'yes':
            user.delete()
            alert_success('The user has been deleted')
        return flask.redirect(flask.url_for('index'))
    
    return flask.render_template('delete_page.html', type="User", name=user.username, form=form)
