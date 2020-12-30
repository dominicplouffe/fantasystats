import requests
from datetime import datetime, timedelta
from fantasystats.services.crawlers.nba import SCHEDULE_URL
from fantasystats.services.nba import parser
from fantasystats.context import logger
from fantasystats.services.crawlers import nba
from fantasystats.managers.nba.season import get_season_from_game_date

SEASONS = [
    {'start': datetime(2017, 10, 1), 'end': datetime(2018, 6, 30)},
    # {'start': datetime(2018, 10, 1), 'end': datetime(2019, 6, 30)},
    # {'start': datetime(2019, 10, 1), 'end': datetime(2020, 10, 31)},
    # {'start': datetime(2020, 12, 1), 'end': datetime(2021, 3, 31)},
]


for season in SEASONS:

    all_res = None

    current_date = season['start']

    while current_date <= season['end']:

        dt = current_date.strftime('%Y-%m-%d')
        nba_url = SCHEDULE_URL % dt
        print(nba_url)
        schedule = requests.get(nba_url).json()

        for d in schedule['payload']['dates']:
            for g in d['games']:

                game_season = get_season_from_game_date(
                    datetime.strptime(
                        g['profile']['dateTimeEt'],
                        '%Y-%m-%dT%H:%M'
                    )
                )
                logger.info(
                    'Game Id: %s - Season: %s' % (
                        g['profile']['gameId'],
                        game_season
                    )
                )

                game_data = nba.get_game(
                    g['profile']['gameId'],
                    game_season,
                    new_only=True
                )

                parser.process_data(game_data, update=True)

        current_date += timedelta(days=1)
        if current_date > season['end']:
            break
