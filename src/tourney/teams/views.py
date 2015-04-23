'''
Created on 22.10.2014

@author: Philip
'''

import flask
import flask_login

import teams.forms
import teams.models
import utils.forms
from utils.views import get_column_names, create_table, create_action_urls, \
    alert_success, error_not_found, error_access_denied


bp_teams = flask.Blueprint("teams", __name__)

@bp_teams.route('/')
@bp_teams.route('/table')
@flask_login.login_required
def table():
    models = teams.models.Team.filter_user(flask_login.current_user).all()
    columns = get_column_names(teams.models.Team())
    table = create_table(models, {'Edit': '.edit', 'Delete': '.delete'}, team_id='id')
    actions = create_action_urls({'Add': '.add'})
    return flask.render_template('table_page.html', type="Teams", columns=columns, table=table, actions=actions)


@bp_teams.route('/add', methods=['GET', 'POST'])
@flask_login.login_required
def add():
    form = teams.forms.TeamForm()
    if form.validate_on_submit():
        teams.models.Team.create(form=form)
        alert_success('The team has been saved')
        return flask.redirect(flask.url_for('.table'))
    
    return flask.render_template('add_page.html', type="Team", form=form)


@bp_teams.route('/edit/<int:team_id>', methods=['GET', 'POST'])
@flask_login.login_required
def edit(team_id):
    team = teams.models.Team.query.filter_by(id=team_id).first()
    if team is None:
        return error_not_found('Team ID {}'.format(team_id), 'index')
    if not team.has_access(flask_login.current_user):
        return error_access_denied('Team ID {}'.format(team_id), 'index')
    
    form = teams.forms.TeamForm(flask.request.form, team)
    # Set default of name field to check if changed (see custom validator
    # function validate_name)
    form.name.default = team.name
    if form.validate_on_submit():
        team.update(form=form)
        alert_success('The team has been saved')
    
    actions = create_action_urls({'Delete': '.delete'}, team, team_id='id')
    return flask.render_template('edit_page.html', type="Team", name=team.name, form=form, actions=actions)


@bp_teams.route('/delete/<int:team_id>', methods=['GET', 'POST'])
@flask_login.login_required
def delete(team_id):
    team = teams.models.Team.query.filter_by(id=team_id).first()
    if team is None:
        return error_not_found('Team ID {}'.format(team_id), 'index')
    if not team.has_access(flask_login.current_user):
        return error_access_denied('Team ID {}'.format(team_id), 'index')
    
    form = utils.forms.ConfirmationForm()
    if form.validate_on_submit():
        if form.radio.data == 'yes':
            team.delete()
            alert_success('The team has been deleted')
        return flask.redirect(flask.url_for('.table'))
    
    return flask.render_template('delete_page.html', type="Team", name=team.name, form=form)
