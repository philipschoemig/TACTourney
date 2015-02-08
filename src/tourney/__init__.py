'''
Created on 02.10.2014

Source: https://realpython.com/blog/python/python-web-applications-with-flask-part-i/

@author: Philip
'''

import logging
import logging.handlers

import flask
import flask_bootstrap
#import flask_ini
import flask_login

import config
import data
import teams.views
import tournaments.views
import users.constants
import users.models
import users.views


app = flask.Flask(__name__)
app.config.from_object('config')
#app.iniconfig = flask_ini.FlaskIni()
#app.iniconfig.readfp(open(config.DEFAULTS_CONFIG_FILE))
#app.iniconfig.read(config.CONFIG_FILE)

app.register_blueprint(teams.views.bp_teams, url_prefix='/teams')
app.register_blueprint(tournaments.views.bp_tournaments, url_prefix='/tournaments')
app.register_blueprint(users.views.bp_users, url_prefix='/users')

bootstrap = flask_bootstrap.Bootstrap(app)
app.extensions['bootstrap']['cdns']['bootstrap-theme'] = flask_bootstrap.StaticCDN()

login_manager = flask_login.LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'

data.db.init_app(app)

# Set up file logging
file_handler = logging.handlers.RotatingFileHandler(config.LOG_FILE, 'a', 5 * 1024 * 1024, 5)
file_handler.setFormatter(logging.Formatter('%(asctime)s '
                                            'Process=%(processName)s#%(process)d Thread=%(threadName)s#%(thread)d '
                                            'Level=%(levelname)s "%(message)s" [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(config.LOG_LEVEL)
file_handler.setLevel(config.LOG_LEVEL)
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


@app.before_first_request
def setup():
    # Set up default admin user
    user = users.models.User.query.filter_by(username=config.ADMIN_USERNAME).first()
    if user is None:
        users.models.User.create(username=config.ADMIN_USERNAME,
                                 password=config.ADMIN_PASSWORD,
                                 role_enum=users.constants.Roles.admin)
