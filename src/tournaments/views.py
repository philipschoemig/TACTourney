'''
Created on 22.10.2014

@author: Philip
'''

import flask
import flask_login

import tournaments.forms
import tournaments.models
import utils.forms
from utils.views import get_column_names, create_table, create_action_urls, \
    alert_success, error_not_found, error_access_denied


bp_tournaments = flask.Blueprint("tournaments", __name__)

@bp_tournaments.route('/')
@bp_tournaments.route('/table')
@flask_login.login_required
def table():
    models = tournaments.models.Tournament.filter_user(flask_login.current_user).all()
    columns = get_column_names(tournaments.models.Tournament())
    table = create_table(models, {'Edit': '.edit', 'Delete': '.delete'}, tournament_id='id')
    actions = create_action_urls({'Add': '.add'})
    return flask.render_template('table_page.html', type="Tournaments", columns=columns, table=table, actions=actions)


@bp_tournaments.route('/add', methods=['GET', 'POST'])
@flask_login.login_required
def add():
    form = tournaments.forms.TournamentForm()
    if form.validate_on_submit():
        tournaments.models.Tournament.create(form=form)
        alert_success('The tournament has been saved')
        return flask.redirect(flask.url_for('.table'))
    
    return flask.render_template('add_page.html', type="Tournament", form=form)


@bp_tournaments.route('/edit/<int:tournament_id>', methods=['GET', 'POST'])
@flask_login.login_required
def edit(tournament_id):
    tournament = tournaments.models.Tournament.query.filter_by(id=tournament_id).first()
    if tournament is None:
        return error_not_found('Tournament ID {}'.format(tournament_id), 'index')
    if not tournament.has_access(flask_login.current_user):
        return error_access_denied('Tournament ID {}'.format(tournament_id), 'index')
    
    form = tournaments.forms.TournamentForm(flask.request.form, tournament)
    if form.validate_on_submit():
        tournament.update(form=form)
        alert_success('The tournament has been saved')
    
    actions = create_action_urls({'Delete': '.delete'}, tournament, tournament_id='id')
    return flask.render_template('edit_page.html', type="Tournament", name=tournament.name, form=form, actions=actions)


@bp_tournaments.route('/delete/<int:tournament_id>', methods=['GET', 'POST'])
@flask_login.login_required
def delete(tournament_id):
    tournament = tournaments.models.Tournament.query.filter_by(id=tournament_id).first()
    if tournament is None:
        return error_not_found('Tournament ID {}'.format(tournament_id), 'index')
    if not tournament.has_access(flask_login.current_user):
        return error_access_denied('Tournament ID {}'.format(tournament_id), 'index')
    
    form = utils.forms.ConfirmationForm()
    if form.validate_on_submit():
        if form.radio.data == 'yes':
            tournament.delete()
            alert_success('The tournament has been deleted')
        return flask.redirect(flask.url_for('.table'))
    
    return flask.render_template('delete_page.html', type="Tournament", name=tournament.name, form=form)
