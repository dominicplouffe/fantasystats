import pytz
import requests
from datetime import datetime, timedelta
from fantasystats.managers.nhl import game as nhl_mgr
from fantasystats.managers.nba import game as nba_mgr
from fantasystats.context import API_URL, logger


def cache(league_name, league_mgr):

    now = datetime.now(pytz.UTC)
    now = datetime(now.year, now.month, now.day)

    date = now - timedelta(days=1)

    for i in range(0, 3):
        for g in league_mgr.get_by_game_date(date):

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
            date.strftime('%Y-%m-%d')
        )

        try:
            res = requests.get(url, timeout=10)
            logger.info('%s:%s' % (url, res.status_code))
        except requests.exceptions.Timeout:
            pass

        date += timedelta(days=1)


if __name__ == '__main__':

    cache('nhl', nhl_mgr)
    cache('nba', nba_mgr)
