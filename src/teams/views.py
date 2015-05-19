'''
Created on 22.10.2014

@author: Philip
'''

import flask
import flask_login

import teams.forms
import teams.models
import utils.forms
from utils.views import create_action_urls, alert_success, error_not_found, \
    error_access_denied


bp_teams = flask.Blueprint("teams", __name__)


@bp_teams.route('/')
@bp_teams.route('/table')
@flask_login.login_required
def table():
    return utils.views.view_table("Teams",
                                  teams.models.Team,
                                  team_id='id')


@bp_teams.route('/add', methods=['GET', 'POST'])
@flask_login.login_required
def add():
    return utils.views.view_add("Team",
                                teams.models.Team,
                                teams.forms.TeamForm())


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
    return flask.render_template('edit_page.html',
                                 type="Team",
                                 name=team.name,
                                 form=form,
                                 actions=actions)


@bp_teams.route('/delete/<int:team_id>', methods=['GET', 'POST'])
@flask_login.login_required
def delete(team_id):
    return utils.views.view_delete("Team",
                                   teams.models.Team,
                                   team_id)
