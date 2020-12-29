from fantasystats.context import logger
from fantasystats.services.crawlers import nba
from fantasystats.services.nba import parser


def get_schedule():

    schedule = nba.get_schedule()

    for d in schedule['payload']['dates']:
        for g in d['games']:
            logger.info(
                'Game Id: %s - Season: %s' % (
                    g['profile']['gameId'],
                    schedule['payload']['season']['yearDisplay']
                )
            )

            game_data = nba.get_game(
                g['profile']['gameId'],
                schedule['payload']['season']['yearDisplay'],
                new_only=True
            )

            parser.process_data(game_data, update=True)


if __name__ == '__main__':

    get_schedule()
