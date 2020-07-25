from fantasystats.context import logger
from fantasystats.services.crawlers import mlb
from fantasystats.managers.mlb import game
from fantasystats.services.mlb import parser


def get_schedule():

    schedule = mlb.get_schedule()

    for d in schedule['dates']:
        for g in d['games']:
            game_data = mlb.get_game(
                g['gamePk'], g['season'], new_only=True)

            logger.info('game_id,%s' % g['gamePk'])

            if not game.get_game_by_mlb_id(g['gamePk']):
                parser.process_game(game_data)


if __name__ == '__main__':
    get_schedule()
