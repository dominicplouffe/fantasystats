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
        except requests.exceptions.Timeout:
            pass
        finally:
            logger.info('%s:%s' % (url, res.status_code))

        date += timedelta(days=1)

    # Get Seasons
    url = '%s%s/seasons' % (
        API_URL,
        league_name
    )
    res = requests.get(url, timeout=10)
    season = res.json()['data'][-1]

    # Cache Standings
    url = '%s%s/standings/%s?force_query=true' % (
        API_URL,
        league_name,
        season
    )

    try:
        res = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        pass
    finally:
        logger.info('%s:%s' % (url, res.status_code))


def cache_league_data():

    league_date = ceil_dt(
        datetime.utcnow() - timedelta(hours=5),
        timedelta(minutes=30)
    )

    league_date = league_date - timedelta(hours=1)

    for i in range(0, 3):
        dt = league_date.strftime('%Y-%m-%d-%H:%M')

        for l in ['league', 'nhl', 'nba']:
            offset = 0
            for j in range(0, 3):
                url = '%s%s/games/date/%s?force_query=true&limit=20&offset=%s' % (
                    API_URL,
                    'league',
                    dt,
                    offset
                )

                if l != 'league':
                    url = '%s&league=%s' % (url, l)
                try:
                    res = requests.get(url, timeout=10)
                    logger.info('%s:%s' % (url, res.status_code))
                    offset += 20
                except requests.exceptions.Timeout:
                    pass
        league_date += timedelta(minutes=30)


def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta


if __name__ == '__main__':

    cache('nhl', nhl_mgr)
    cache('nba', nba_mgr)
    cache_league_data()
