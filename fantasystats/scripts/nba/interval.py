import requests
from datetime import datetime, timedelta
from fantasystats.services.nba import parser
from fantasystats.context import API_URL, logger
from fantasystats.services.crawlers import nba


if __name__ == '__main__':

    d = datetime.utcnow() - timedelta(hours=7)
    d = datetime(d.year, d.month, d.day)

    url = '%s/nba/games/date/%s' % (
        API_URL,
        d.strftime('%Y-%m-%d')
    )

    logger.info(url)
    res = requests.get(url).json()

    for game_info in res['data']:
        print(game_info['game_key'])
        crawl_game = False
        if game_info['game_status'] in ['Final']:
            logger.info('game final, do not crawl')
            continue
        if game_info['game_status'] == 'I':
            logger.info('in_progress')
            crawl_game = True
        else:
            logger.info('start_time,%s' % game_info['start_time'])
            try:
                start_time = datetime.strptime(
                    game_info['start_time'], '%Y-%m-%d %H:%M'
                ) - timedelta(hours=10)

                if datetime.utcnow() >= start_time:
                    crawl_game = True
            except ValueError:
                logger.inf('unknown starttime,crawly anyways')
                crawl_game = True
        if crawl_game:
            logger.info(
                'crawling,%s,%s' % (
                    game_info['game_key'],
                    game_info['nba_id']
                )
            )

            nba_res = nba.get_game(
                game_info['nba_id'],
                game_info['season'],
                new_only=True
            )
            parser.process_data(nba_res, update=True)

    logger.info('Sleeping for 5 mins')
