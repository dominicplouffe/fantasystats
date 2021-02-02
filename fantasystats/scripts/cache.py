import pytz
import requests
from datetime import datetime
from fantasystats.managers.nhl import game as nhl_mgr
from fantasystats.managers.nba import game as nba_mgr
from fantasystats.context import API_URL, logger


def cache(league_name, league_mgr):

    now = datetime.now(pytz.UTC)
    now = datetime(now.year, now.month, now.day)

    for g in league_mgr.get_by_game_date(now):

        url = '%s%s/game/id/%s?force_query=true' % (
            API_URL,
            league_name,
            g.game_key
        )
        try:
            res = requests.get(url, timeout=10)
            logger.info('%s:%s' % (url, res.status_code))
        except requests.exceptions.Timeout:
            pass

    url = '%s%s/games/date/%s?force_query=true' % (
        API_URL,
        league_name,
        now.strftime('%Y-%m-%d')
    )

    try:
        res = requests.get(url, timeout=10)
        logger.info('%s:%s' % (url, res.status_code))
    except requests.exceptions.Timeout:
        pass


if __name__ == '__main__':

    cache('nhl', nhl_mgr)
    cache('nba', nba_mgr)
