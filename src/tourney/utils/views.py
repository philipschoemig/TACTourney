'''
Created on 22.10.2014

@author: Philip
'''

import flask

import utils.redirect


def get_column_names(model):
    """
    Retrieves the column names of the given database model.
    """
    columns = []
    for column in model.__table__.columns:
        label = column.info.get('label')
        if label:
            columns.append((column.name, label))
    return columns


def create_table(models, actions, **url_args):
    """
    Creates a table with the given database models.
    """
    table = []
    for model in models:
        row = {}
        for column in model.__table__.columns:
            # Get the attr key from the column info member if available
            attr = column.info.get('attr', column.name)
            # Split the attr key into single attributes
            attributes = attr.split(".")
            # Resolve the attributes from the model recursively
            value = model
            for name in attributes:
                value = getattr(value, name)
            # Add column to the row
            row[column.name] = value
        # Add actions column to the row
        row['actions'] = create_action_urls(actions, model, **url_args)
        # Add row to the table
        table.append(row)
    return table


def create_action_urls(actions, model=None, **url_args):
    """
    Creates a list of URLs for the given actions.
    """
    urls = {}
    if len(actions) > 0:
        # Resolve the url_args values as attributes from the model
        values = {}
        for arg in url_args:
            values[arg] = getattr(model, url_args[arg])
        # Generate the URL for every action
        for action in actions:
            urls[action] = flask.url_for(actions[action], **values)
    return urls


def alert_success(message):
    """
    Shows a success message.
    """
    flask.flash(message, 'success')


def alert_info(message):
    """
    Shows an info message.
    """
    flask.flash(message, 'info')


def alert_warning(message):
    """
    Shows a warning message.
    """
    flask.flash(message, 'warning')


def alert_danger(message):
    """
    Shows an error message.
    """
    flask.flash(message, 'danger')


def error_not_found(message, redirect):
    """
    Shows an error message that a page couldn't be found.
    """
    alert_danger('Not found: {}'.format(message))
    return utils.redirect.redirect_back(redirect)
    #return flask.redirect(redirect)


def error_access_denied(message, redirect):
    """
    Shows an error message that a page couldn't be accessed.
    """
    alert_danger('Access denied: {}'.format(message))
    return utils.redirect.redirect_back(redirect)
    #return flask.redirect(redirect)
