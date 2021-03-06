'''
Created on 22.10.2014

@author: Philip
'''

import flask
import flask_login

import tournaments.forms
import tournaments.models
import utils.forms
from utils.views import create_action_urls, alert_success, error_not_found, \
    error_access_denied


bp_tournaments = flask.Blueprint("tournaments", __name__)


@bp_tournaments.route('/')
@bp_tournaments.route('/table')
@flask_login.login_required
def table():
    return utils.views.view_table("Tournaments",
                                  tournaments.models.Tournament,
                                  tournament_id='id')


@bp_tournaments.route('/add', methods=['GET', 'POST'])
@flask_login.login_required
def add():
    return utils.views.view_add("Tournament",
                                tournaments.models.Tournament,
                                tournaments.forms.TournamentForm())


@bp_tournaments.route('/edit/<int:tournament_id>', methods=['GET', 'POST'])
@flask_login.login_required
def edit(tournament_id):
    tournament = tournaments.models.Tournament.query.filter_by(
        id=tournament_id).first()
    if tournament is None:
        return error_not_found(
            'Tournament ID {}'.format(tournament_id), 'index')
    if not tournament.has_access(flask_login.current_user):
        return error_access_denied(
            'Tournament ID {}'.format(tournament_id), 'index')

    form = tournaments.forms.TournamentForm(flask.request.form, tournament)
    if form.validate_on_submit():
        tournament.update(form=form)
        alert_success('The tournament has been saved')

    actions = create_action_urls(
        {'Delete': '.delete'}, tournament, tournament_id='id')
    return flask.render_template('edit_page.html',
                                 type="Tournament",
                                 name=tournament.name,
                                 form=form,
                                 actions=actions)


@bp_tournaments.route('/delete/<int:tournament_id>', methods=['GET', 'POST'])
@flask_login.login_required
def delete(tournament_id):
    return utils.views.view_delete("Tournament",
                                   tournaments.models.Tournament,
                                   tournament_id)
