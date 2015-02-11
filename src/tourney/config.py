'''
Created on 02.10.2014

@author: Philip
'''

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULTS_CONFIG_FILE = os.path.join(BASE_DIR, 'defaults.cfg')
CONFIG_FILE = os.path.join(BASE_DIR, 'tourney.cfg')

APP_NAME = 'TACTourney'
APP_VERSION = 'Version 1.0'

DEBUG = True
SECRET_KEY = 'flask-session-insecure-secret-key' # TODO

LOG_FILE = os.path.join(BASE_DIR, 'tourney.log')
LOG_LEVEL = 'INFO'

BOOTSTRAP_USE_MINIFIED = True
BOOTSTRAP_SERVE_LOCAL = True

DATABASE_FILE = os.path.join(BASE_DIR, 'tourney.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_FILE)
SQLALCHEMY_ECHO = False

RECAPTCHA_PUBLIC_KEY = '6Le-Q_wSAAAAAGwJdBKNqGYsZLugT5-gv3H1PHie' # domain: crufty.de
RECAPTCHA_PRIVATE_KEY = '6Le-Q_wSAAAAAPZ2cunjj7wi_mAbCRz2UaAcyx1p' # domain: crufty.de

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'test'
