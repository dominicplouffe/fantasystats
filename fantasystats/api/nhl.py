from flask import Blueprint, request
import pytz
from datetime import datetime
from fantasystats.api.base_view import BaseView
from fantasystats.services.nhl import game
from fantasystats.tools.cache import memorize

nhl = Blueprint('nhl', __name__)


class GetGameById(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, game_id):

        game_id = game_id.lower()
        game_id = game_id.replace('-n-1', '-N-1')

        game_info = game.get_game_by_key(
            game_id,
            include_odds=True,
            include_predictions=True,
            include_injuries=True,
            force_query=request.args.get(
                'force_query', 'false'
            ).lower() == 'true'
        )

        return self.write_json(game_info, 200)


class GetGamesByDate(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, date):

        game_date = datetime.strptime(date, "%Y-%m-%d")

        games = game.get_games_by_date(game_date)
        ames = sorted(games, key=lambda x: x['start_time'])

        return self.write_json(games)


class GetStandings(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, season):

        by = request.args.get('by', 'nhl')
        standings = game.get_standings(
            season,
            by=by,
            force_query=request.args.get(
                'force_query', 'false'
            ).lower() == 'true'
        )

        return self.write_json(
            standings
        )


class GetTeam(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, season, team_id):

        date = request.args.get('date', None)
        if date:
            date = datetime.strptime(date, "%Y-%m-%d")

        team = game.get_team_details(
            season,
            team_id,
            to_date=date,
            force_query=request.args.get(
                'force_query', 'false'
            ).lower() == 'true'
        )

        return self.write_json(team)


class GetTeams(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, season):

        return self.write_json(
            game.get_all_teams(
                season,
                force_query=request.args.get(
                    'force_query', 'false'
                ).lower() == 'true'
            )
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


class GetSeasons(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self):

        return self.write_json(
            game.get_seasons()
        )


nhl.add_url_rule(
    '/nhl/game/id/<string:game_id>',
    view_func=GetGameById.as_view('/nhl/game/id/<string:game_id>'),
    methods=['GET']
)

nhl.add_url_rule(
    '/nhl/games/date/<string:date>',
    view_func=GetGamesByDate.as_view('/nhl/games/date/<string:date>'),
    methods=['GET']
)

nhl.add_url_rule(
    '/nhl/standings/<string:season>',
    view_func=GetStandings.as_view('/nhl/standings/<string:season>'),
    methods=['GET']
)

nhl.add_url_rule(
    '/nhl/teams/<string:season>',
    view_func=GetTeams.as_view('/nhl/teams/<string:season>'),
    methods=['GET']
)

nhl.add_url_rule(
    '/nhl/team/<string:season>/<string:team_id>',
    view_func=GetTeam.as_view('/nhl/team/<string:season>/<string:team_id>'),
    methods=['GET']
)

nhl.add_url_rule(
    '/nhl/player/<string:player_id>',
    view_func=GetPlayer.as_view('/nhl/player/<string:player_id>'),
    methods=['GET']
)

nhl.add_url_rule(
    '/nhl/teams/<string:season>/<string:away_team>/<string:home_team>',
    view_func=GetTeamVS.as_view(
        '/nhl/teams/<string:season>/<string:away_team>/<string:home_team>'),
    methods=['GET']
)

nhl.add_url_rule(
    '/nhl/seasons',
    view_func=GetSeasons.as_view('/nhl/seasons'),
    methods=['GET']
)
