#!/usr/bin/env python
'''
Created on 02.10.2014

@author: Philip
'''

import sys

from __init__ import app, manager
import data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        manager.run()
    else:
        app.debug = True
        # Because we did not initialize Flask-SQLAlchemy with an application
        # it will use `current_app` instead.  Since we are not in an application
        # context right now, we will instead pass in the configured application
        # into our `create_all` call.
        data.db.create_all(app=app)
        app.run()
