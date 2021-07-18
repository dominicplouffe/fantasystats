from flask import Blueprint, request
from datetime import datetime
import re
from fantasystats.api.base_view import BaseView
from fantasystats.tools.cache import memorize
from fantasystats.services.esports import matches


esports = Blueprint('esports', __name__)


class GetGameById(BaseView):

    cache_time = 86400

    @memorize
    def dispatch_request(self, game_id):

        match_info = matches.get_match(game_id)

        return self.write_json(match_info, 200)


class GetGamesByDate(BaseView):

    cache_time = 60 * 5

    @memorize
    def dispatch_request(self, date):

        game_date = datetime.strptime(date, "%Y-%m-%d")
        event_id = request.args.get('event_id', None)
        category = request.args.get('category', None)

        games = matches.get_matches_by_date(
            game_date,
            category=category,
            event_id=event_id
        )
        games = sorted(games, key=lambda x: x['start_time'])

        return self.write_json(games)


esports.add_url_rule(
    '/esports/game/id/<string:game_id>',
    view_func=GetGameById.as_view('/esports/game/id/<string:game_id>'),
    methods=['GET']
)

esports.add_url_rule(
    '/esports/games/date/<string:date>',
    view_func=GetGamesByDate.as_view('/esports/games/date/<string:date>'),
    methods=['GET']
)
