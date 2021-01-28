from fantasystats.context import logger
from fantasystats.services.crawlers import nba
from fantasystats.services.nba import parser
from fantasystats.managers.nba.season import get_season_from_game_date
from datetime import datetime


def get_schedule():

    schedule = nba.get_schedule()

    for d in schedule['payload']['dates']:
        for g in d['games']:

            season = get_season_from_game_date(
                datetime.strptime(
                    g['profile']['dateTimeEt'],
                    '%Y-%m-%dT%H:%M'
                )

            )
            logger.info(
                'Game Id: %s - Season: %s' % (
                    g['profile']['gameId'],
                    season
                )
            )

            game_data = nba.get_game(
                g['profile']['gameId'],
                season,
                new_only=True
            )

            parser.process_data(game_data, update=True)


if __name__ == '__main__':

    get_schedule()
