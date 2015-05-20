'''
Created on 01.12.2014

@author: Philip
'''

import flask_migrate
import flask_script
import getpass
import os
import random

from app import app, configurator
from data import db
import users.constants
import users.models


migrate = flask_migrate.Migrate(app, db)

manager = flask_script.Manager(app)
manager.add_command('db', flask_migrate.MigrateCommand)

def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits.

    Taken from the django.utils.crypto module.
    """
    return ''.join(random.SystemRandom().choice(allowed_chars) for i in range(length))

def get_secret_key():
    """
    Create a random secret key.

    Taken from the Django project.
    """
    chars = '''!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}'''
    return get_random_string(50, chars)

@manager.command
def setup():
    '''Setup the configuration for TACTourney'''
    # Create configuration file
    print "Creating configuration file..."
    user_config_path = app.config['USER_CONFIG_PATH']
    print "User config path: " + user_config_path
    if not os.path.exists(user_config_path):
        data = open(app.config['DEFAULT_CONFIG_PATH'], 'r').read()
        open(app.config['USER_CONFIG_PATH'], 'w').write(data)
        raw_input("Please adjust the configuration and then press [Enter] to continue")
        print "Parsing configuration file..."
        configurator.parse()
        print "Done"
    else:
        print "Error: File already exists"
    print
    
    # Create secret key file
    print "Creating secret key file..."
    secret_key_path = app.config['SECRET_KEY_PATH']
    print "Secret key path: " + secret_key_path
    if not os.path.exists(secret_key_path):
        open(secret_key_path, 'wb').write(get_secret_key())
        print "Done"
    else:
        print "Error: File already exists"
    print
    
    # Create database tables
    print "Creating database tables..."
    db.create_all(app=app)
    print "Done"
    print
    
    # Create default admin user
    print "Creating default admin user..."
    username = app.config['ADMIN_USERNAME']
    print "Username: " + username
    user = users.models.User.query.filter_by(username=username).first()
    if user is None:
        password = getpass.getpass("Please enter the password for the admin user: ")
        while len(password) == 0:
            password = getpass.getpass("Incorrect password entered. Please try again: ")
        users.models.User.create(username=username,
                                 password=password,
                                 role_enum=users.constants.Roles.admin)
        print "Done"
    else:
        print "Error: User already exists"
    print


if __name__ == '__main__':
    manager.run()
