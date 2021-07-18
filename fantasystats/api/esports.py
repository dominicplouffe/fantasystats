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


esports.add_url_rule(
    '/esports/game/id/<string:game_id>',
    view_func=GetGameById.as_view('/esports/game/id/<string:game_id>'),
    methods=['GET']
)
