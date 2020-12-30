import json
import requests
from fantasystats.tools import s3
from fantasystats.services import search
from datetime import datetime, timedelta

SCHEDULE_URL = 'https://ca.global.nba.com/stats2/season/schedule.json?' \
    'countryCode=CA&gameDate=%s&locale=en&tz=0'

NBA_GAME_URL = 'https://ca.global.nba.com/stats2/game/snapshot.json?' \
    'countryCode=CA&gameId=%s&locale=en&tz=0'

PLAYER_IMAGE_URL = 'https://ak-static.cms.nba.com/wp-content/uploads/' \
    'headshots/nba/latest/260x190/%s.png'


def get_player_thumbnail(player_id, player_name):

    res = requests.get(PLAYER_IMAGE_URL % player_id)

    if res.status_code == 200:

        filename = search.get_search_value(player_name)
        f = open('/tmp/%s.png' % filename, 'wb')
        f.write(res.content)
        f.close()

        s3.upload_to_s3(
            '/tmp/%s.png' % filename,
            'mba/players/%s.png' % filename,
            extra={'ACL': 'public-read', 'ContentType': "image/pgn"}
        )

        return '%s.png' % filename

    return None


def get_schedule():

    # start_date = datetime.utcnow() - timedelta(days=10)
    # end_date = datetime.utcnow() + timedelta(days=10)

    start_date = datetime.utcnow() - timedelta(days=2)
    end_date = datetime.utcnow() + timedelta(days=2)

    current_date = start_date
    all_res = None

    while current_date <= end_date:

        dt = current_date.strftime('%Y-%m-%d')

        nba_url = SCHEDULE_URL % dt
        print(nba_url)
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

        obj = s3.list_objects('mba/files/%s/%s.json' % (
            season,
            nba_id,
        ))

        if 'Contents' in obj:
            r = s3.get_object('mba/files/%s/%s.json' % (
                season,
                nba_id,
            )
            )
            nba_res = json.loads(r['Body'].read())
            return nba_res

    game_url = NBA_GAME_URL % nba_id
    print(game_url)
    res = requests.get(game_url).json()

    f = open('/tmp/%s.json' % nba_id, 'w')
    f.write(json.dumps(res))
    f.close()

    s3.upload_to_s3(
        '/tmp/%s.json' % nba_id,
        'mba/files/%s/%s.json' % (season, nba_id)
    )

    return res
