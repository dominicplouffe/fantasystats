import json
from flask import Blueprint, request, Response
from datetime import datetime
from fantasystats.api.base_view import BaseView
from fantasystats.services.mlb import game
from fantasystats.context import REDIS, logger

mlb = Blueprint('mlb', __name__)


def memorize(func):
    def wrapper(*args, **kwargs):

        view = args[0]
        key = request.url
        data = REDIS.get(key)
        if data is None or request.args.get('force_query', 'false').lower() == 'true':
            logger.info('data not found or force query,%s' % key)
            res = func(*args, **kwargs)
            REDIS.set(key, res.get_data(), view.cache_time)
            return res

        return Response(
            data,
            mimetype="text/json",
            headers={'Access-Control-Allow-Origin': '*'},
            status=200
        )
    return wrapper


class GetGameById(BaseView):

    cache_time = 60

    @memorize
    def dispatch_request(self, game_id):

        game_info = game.get_game_by_key(game_id)

        return self.write_json(game_info, 200)


class GetGamesByDate(BaseView):

    cache_time = 60 * 60

    @memorize
    def dispatch_request(self, date):

        game_date = datetime.strptime(date, "%Y-%m-%d")

        return self.write_json(
            game.get_games_by_date(game_date)
        )


class GetStandings(BaseView):

    cache_time = 60 * 60

    @memorize
    def dispatch_request(self, season):

        by = request.args.get('by', 'mlb')
        standings = game.get_standings(season, by=by)

        return self.write_json(
            standings
        )


class GetTeam(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, season, team_id):

        team = game.get_team_details(season, team_id)

        return self.write_json(team)


class GetTeams(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, season):

        return self.write_json(
            game.get_all_teams(season)
        )


class GetPlayer(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, player_id):

        return self.write_json(
            game.get_player(player_id)
        )


class GetTeamVS(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, season, away_team, home_team):

        return self.write_json(
            game.get_versus(season, away_team, home_team)
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

mlb.add_url_rule(
    '/mlb/teams/<string:season>/<string:away_team>/<string:home_team>',
    view_func=GetTeamVS.as_view(
        '/mlb/teams/<string:season>/<string:away_team>/<string:home_team>'),
    methods=['GET']
)
