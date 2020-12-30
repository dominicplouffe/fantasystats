import requests
from datetime import datetime, timedelta
from fantasystats.services.mlb import parser
from fantasystats.context import API_URL, logger
from fantasystats.services.crawlers import mlb


if __name__ == '__main__':

    d = datetime.utcnow() - timedelta(hours=7)
    d = datetime(d.year, d.month, d.day)

    url = '%s/mlb/games/date/%s' % (
        API_URL,
        d.strftime('%Y-%m-%d')
    )

    print(url)
    res = requests.get(url).json()

    for game_info in res['data']:
        crawl_game = False
        if game_info['game_status'] in ['F', 'FR']:
            continue
        if game_info['game_status'] == 'I':
            crawl_game = True
        else:
            start_time = datetime.strptime(
                game_info['start_time'], '%Y-%m-%d %H:%M'
            ) - timedelta(hours=10)

            if datetime.utcnow() >= start_time:
                crawl_game = True

        if crawl_game:
            logger.info('crawling,%s,%s' %
                        (game_info['game_key'], game_info['mlb_id']))

            mlb_res = mlb.get_game(
                game_info['mlb_id'], game_info['season'], new_only=True)
            parser.process_data(mlb_res, update=True)

    logger.info('Sleeping for 5 mins')
