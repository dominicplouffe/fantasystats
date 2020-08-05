from fantasystats.context import logger
from fantasystats.services.crawlers import nhl
from fantasystats.services.mlb import parser


def get_schedule():

    schedule = nhl.get_schedule()

    for d in schedule['dates']:
        for g in d['games']:
            game_data = nhl.get_game(
                g['gamePk'], g['season'], new_only=True)

            logger.info('game_id,%s' % g['gamePk'])

            parser.process_data(game_data, update=True)


if __name__ == '__main__':
    get_schedule()
