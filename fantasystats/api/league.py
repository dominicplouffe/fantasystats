from flask import Blueprint, request
from datetime import datetime, timedelta
from fantasystats.api.base_view import BaseView
from fantasystats.services.nhl import game as game_nhl
from fantasystats.services.nba import game as game_nba
from fantasystats.services.mlb import game as game_mlb
from fantasystats.tools.cache import memorize

league = Blueprint('league', __name__)


class GetGamesByDate(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, date):

        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 5)
        league = request.args.get('league', None)
        mlb = request.args.get('mlb', None)

        if offset:
            try:
                offset = int(offset)
            except ValueError:
                offset = 0

        if limit:
            try:
                limit = int(limit)
            except ValueError:
                limit = 5

        max_recs = offset + limit
        try:
            game_date = datetime.strptime(date, "%Y-%m-%d-%H:%M")
        except:
            return self.write_json(
                {'games': [], 'has_more': False},
                500
            )

        games = []
        has_more = False

        if league is None or league == 'nba':
            nba_games = game_nba.get_games_by_date(game_date)
            games.extend(nba_games)
        if mlb == 'true' or league == 'mlb':
            mlb_games = game_mlb.get_games_by_date(game_date)
            games.extend(mlb_games)
        if league is None or league == 'nhl':
            nhl_games = game_nhl.get_games_by_date(game_date)
            games.extend(nhl_games)

        games = [g for g in games if g['start_time'] >= game_date]
        games = sorted(games, key=lambda x: x['start_time'])

        if len(games[max_recs:]) > 0:
            has_more = True

        games = games[offset:max_recs]

        res = {
            'games': games,
            'has_more': has_more
        }

        return self.write_json(res)


class Matchup(BaseView):

    def dispatch_request(self, teama, teamb):

        date = datetime.utcnow() - timedelta(hours=5)
        date = datetime(date.year, date.month, date.day)

        mlb_matchup = game_mlb.get_matchup(teama, teamb, date)

        if mlb_matchup:
            return self.write_json(mlb_matchup)

        nba_matchup = game_nba.get_matchup(teama, teamb, date)

        if nba_matchup:
            return self.write_json(nba_matchup)

        nhl_matchup = game_nhl.get_matchup(teama, teamb, date)

        if nhl_matchup:
            return self.write_json(nhl_matchup)

        return self.write_json({})


league.add_url_rule(
    '/league/games/date/<string:date>',
    view_func=GetGamesByDate.as_view('/league/games/date/<string:date>'),
    methods=['GET']
)

league.add_url_rule(
    '/league/games/matchup/<string:teama>/<string:teamb>',
    view_func=Matchup.as_view(
        '/league/games/matchup/<string:teama>/<string:teamb>'
    ),
    methods=['GET']
)
