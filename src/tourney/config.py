'''
Created on 02.10.2014

@author: Philip
'''

import os.path

_cwd = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
SECRET_KEY = 'flask-session-insecure-secret-key' # TODO
DATABASE_FILE = os.path.join(_cwd, 'tourney.db')

BOOTSTRAP_USE_MINIFIED = True
BOOTSTRAP_SERVE_LOCAL = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_FILE)
SQLALCHEMY_ECHO = False

RECAPTCHA_PUBLIC_KEY = '6Le-Q_wSAAAAAGwJdBKNqGYsZLugT5-gv3H1PHie' # domain: crufty.de
RECAPTCHA_PRIVATE_KEY = '6Le-Q_wSAAAAAPZ2cunjj7wi_mAbCRz2UaAcyx1p' # domain: crufty.de

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'test'
