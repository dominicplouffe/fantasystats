import requests
from datetime import datetime, timedelta

SCHEDULE_URL = 'https://ca.global.nba.com/stats2/season/schedule.json?' \
    'countryCode=CA&gameDate=%s&locale=en&tz=0'

NBA_GAME_URL = 'https://ca.global.nba.com/stats2/game/snapshot.json?' \
    'countryCode=CA&gameId=%s&locale=en&tz=0'


def get_schedule():

    # start_date = datetime.utcnow() - timedelta(days=10)
    # end_date = datetime.utcnow() + timedelta(days=10)

    start_date = datetime.utcnow() - timedelta(days=2)
    end_date = datetime.utcnow() + timedelta(days=2)
    year = start_date.year

    current_date = start_date
    all_res = None

    while current_date <= end_date:

        dt = current_date.strftime('%Y-%m-%d')

        nba_url = SCHEDULE_URL % dt
        res = requests.get(nba_url).json()

        if all_res is None:
            if len(res['payload']['dates']) > 0:
                all_res = res
        else:
            if len(res['payload']['dates']) > 0:
                all_res['payload']['dates'].append(
                    {'games': res['payload']['dates'][0]['games']}
                )

        current_date += timedelta(days=1)

    return all_res


def get_game(nba_id, season, new_only=False):

    if not new_only:

        # TODO: try to get from S3
        pass

    game_url = NBA_GAME_URL % nba_id
    print(game_url)
    res = requests.get(game_url).json()

    # TODO Write to S3

    return res
