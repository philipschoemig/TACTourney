'''
Created on 02.10.2014

Source: https://realpython.com/blog/python/python-web-applications-with-flask-part-i/

@author: Philip
'''

import logging.handlers
import os

import flask
import flask_bootstrap
import flask_login

import config
import data
import teams.views
import tournaments.views
import users.models
import users.views


APP_NAME = 'TACTourney'
APP_VERSION = '1.0'

DEFAULT_CONFIG_FILE = 'default.cfg'
USER_CONFIG_FILE = 'user.cfg'
SECRET_KEY_FILE = 'secret_key'

BOOTSTRAP_USE_MINIFIED = True
BOOTSTRAP_SERVE_LOCAL = True

ADMIN_USERNAME = 'admin'


app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config['DEFAULT_CONFIG_PATH'] = os.path.join(
    app.root_path, DEFAULT_CONFIG_FILE)
app.config['USER_CONFIG_PATH'] = os.path.join(
    app.instance_path, USER_CONFIG_FILE)
app.config['SECRET_KEY_PATH'] = os.path.join(
    app.instance_path, SECRET_KEY_FILE)
if not os.path.isdir(app.instance_path):
    os.mkdir(app.instance_path)
if os.path.isfile(app.config['SECRET_KEY_PATH']):
    app.config['SECRET_KEY'] = open(app.config['SECRET_KEY_PATH'], 'rb').read()

configurator = config.Configurator(app)

app.register_blueprint(teams.views.bp_teams, url_prefix='/teams')
app.register_blueprint(
    tournaments.views.bp_tournaments, url_prefix='/tournaments')
app.register_blueprint(users.views.bp_users, url_prefix='/users')

bootstrap = flask_bootstrap.Bootstrap(app)
app.extensions['bootstrap']['cdns'][
    'bootstrap-theme'] = flask_bootstrap.StaticCDN()

login_manager = flask_login.LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'
login_manager.login_message = u'Please log in to access this page.'
login_manager.login_message_category = 'info'

data.db.init_app(app)

# Set up file logging
file_handler = logging.handlers.RotatingFileHandler(
    app.config['LOG_FILE'], 'a', 5 * 1024 * 1024, 5)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s '
    'PID=%(processName)s(%(process)x) TID=%(threadName)s(%(thread)x) '
    'Level=%(levelname)s "%(message)s" [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(app.config['LOG_LEVEL'])
file_handler.setLevel(app.config['LOG_LEVEL'])
app.logger.addHandler(file_handler)
app.logger.info('tourney startup')


@login_manager.user_loader
def load_user(user_id):
    return users.models.User.query.get(int(user_id))


@app.route('/')
def index():
    if not flask_login.current_user.is_authenticated():
        return flask.redirect(flask.url_for('users.login'))
    return flask.redirect(flask.url_for('tournaments.table'))
