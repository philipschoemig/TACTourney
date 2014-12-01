'''
Created on 01.12.2014

@author: Philip
'''

import flask_migrate
import flask_script

from __init__ import app
from data import db


migrate = flask_migrate.Migrate(app, db)

manager = flask_script.Manager(app)
manager.add_command('db', flask_migrate.MigrateCommand)

if __name__ == '__main__':
    manager.run()
