import requests
from fantasystats.context import logger
from fantasystats.services.crawlers import nhl
from fantasystats.services.nhl import parser


def get_schedule():

    res = requests.get(
        'https://api.connexion.me/api/pongme/start/801616-720093-637131-914688'
    )
    schedule = nhl.get_schedule()

    for d in schedule['dates']:
        for g in d['games']:
            game_data = nhl.get_game(
                g['gamePk'], g['season'], new_only=True)

            game_data['broadcasters'] = g['broadcasts']
            logger.info('game_id,%s' % g['gamePk'])
            parser.process_data(game_data, update=True)

    res = requests.get(
        'https://api.connexion.me/api/pongme/end/801616-720093-637131-914688'
    )


if __name__ == '__main__':
    get_schedule()
