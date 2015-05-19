'''
Created on 22.10.2014

@author: Philip
'''

import flask
import flask_login

import utils.redirect


def view_table(title, model, **url_args):
    """
    View function to display a table for the given model class.
    """
    entries = model.filter_user(flask_login.current_user).all()
    columns = get_column_names(model())
    table = create_table(
        entries, {'Edit': '.edit', 'Delete': '.delete'}, **url_args)
    actions = create_action_urls({'Add': '.add'})
    return flask.render_template('table_page.html',
                                 title=title,
                                 columns=columns,
                                 table=table,
                                 actions=actions)


def view_add(title, model, form):
    if form.validate_on_submit():
        model.create(form=form)
        alert_success('The {0} has been added'.format(title.lower()))
        return flask.redirect(flask.url_for('.table'))

    return flask.render_template('add_page.html', type=title, form=form)


def view_delete(title, model, entry_id):
    entry = model.query.filter_by(id=entry_id).first()
    if entry is None:
        return error_not_found('{0} ID {1}'.format(title, entry_id), 'index')
    if not entry.has_access(flask_login.current_user):
        return error_access_denied(
            '{0} ID {1}'.format(title, entry_id), 'index')

    form = utils.forms.ConfirmationForm()
    if form.validate_on_submit():
        if form.radio.data == 'yes':
            entry.delete()
            alert_success('The {0} has been deleted'.format(title.lower()))
        return flask.redirect(flask.url_for('.table'))

    return flask.render_template('delete_page.html',
                                 type=title,
                                 name=entry.name,
                                 form=form)


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


def error(message, redirect):
    """
    Shows an error message.
    """
    alert_danger(message)
    return utils.redirect.redirect_back(redirect)


def error_not_found(message, redirect):
    """
    Shows an error message that a page couldn't be found.
    """
    return error('Not found: {}'.format(message), redirect)


def error_access_denied(message, redirect):
    """
    Shows an error message that a page couldn't be accessed.
    """
    return error('Access denied: {}'.format(message), redirect)
