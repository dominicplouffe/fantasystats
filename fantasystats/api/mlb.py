from flask import Blueprint, request
from datetime import datetime
from fantasystats.api.base_view import BaseView
from fantasystats.services.mlb import game

mlb = Blueprint('mlb', __name__)


class GetGameById(BaseView):

    def dispatch_request(self, game_id):

        game_info = game.get_game_by_key(game_id)

        return self.write_json(game_info, 200)


class GetGamesByDate(BaseView):

    def dispatch_request(self, date):

        game_date = datetime.strptime(date, "%Y-%m-%d")

        return self.write_json(
            game.get_games_by_date(game_date)
        )


class GetStandings(BaseView):
    def dispatch_request(self, season):

        by = request.args.get('by', 'mlb')
        standings = game.get_standings(season, by=by)

        return self.write_json(
            standings
        )


class GetTeam(BaseView):
    def dispatch_request(self, season, team_id):

        team = game.get_team_details(season, team_id)

        return self.write_json(team)


class GetTeams(BaseView):
    def dispatch_request(self, season):

        return self.write_json(
            game.get_all_teams(season)
        )


class GetPlayer(BaseView):
    def dispatch_request(self, player_id):

        return self.write_json(
            game.get_player(player_id)
        )


mlb.add_url_rule(
    '/mlb/game/id/<string:game_id>',
    view_func=GetGameById.as_view('/mlb/game/id/<string:game_id>'),
    methods=['GET']
)

mlb.add_url_rule(
    '/mlb/games/date/<string:date>',
    view_func=GetGamesByDate.as_view('/mlb/games/date/<string:date>'),
    methods=['GET']
)

mlb.add_url_rule(
    '/mlb/standings/<string:season>',
    view_func=GetStandings.as_view('/mlb/standings/<string:season>'),
    methods=['GET']
)

mlb.add_url_rule(
    '/mlb/teams/<string:season>',
    view_func=GetTeams.as_view('/mlb/teams/<string:season>'),
    methods=['GET']
)

mlb.add_url_rule(
    '/mlb/team/<string:season>/<string:team_id>',
    view_func=GetTeam.as_view('/mlb/team/<string:season>/<string:team_id>'),
    methods=['GET']
)

mlb.add_url_rule(
    '/mlb/player/<string:player_id>',
    view_func=GetPlayer.as_view('/mlb/player/<string:player_id>'),
    methods=['GET']
)
