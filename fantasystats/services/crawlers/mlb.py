import json
import requests
from fantasystats.tools import s3
from unidecode import unidecode
from fantasystats.services import search
from datetime import datetime, timedelta

PLAYER_SEARCH_URL = 'https://typeahead.mlb.com/api/v1/typeahead/suggestions/%s'
SCHEDULE_URL = 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=' \
               '%s&endDate=%s&leagueId=103&&leagueId=104'
MLB_GAME_URL = 'https://statsapi.mlb.com/api/v1.1/game/%s/feed/live'


def get_player_thumbnail(player_name):
    player_name = unidecode(player_name)

    res = requests.get(PLAYER_SEARCH_URL % player_name).json()

    if len(res.get('players',  [])) > 0:
        content = requests.get(
            res['players'][0]['headshots'][0]['url']).content

        filename = search.get_search_value(player_name)
        f = open('/tmp/%s.png' % filename, 'wb')
        f.write(content)
        f.close()

        s3.upload_to_s3('/tmp/%s.png' %
                        filename, 'mlb/players/%s.png' % filename, extra={'ACL': 'public-read', 'ContentType': "image/pgn"})

        return '%s.png' % filename

    return None


def get_schedule():

    start_date = datetime.utcnow() - timedelta(days=10)
    end_date = datetime.utcnow() + timedelta(days=1)
    year = start_date.year
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    mlb_url = SCHEDULE_URL % (
        start_date,
        end_date
    )

    print(mlb_url)

    res = requests.get(mlb_url).json()
    filename = 'schedule.json'
    f = open('/tmp/%s.png' % filename, 'w')
    f.write(json.dumps(res))
    f.close()

    s3.upload_to_s3('/tmp/%s.png' %
                    filename, 'mlb/files/%s/%s.png' % (
                        year, filename),
                    extra={'ACL': 'public-read', 'ContentType': "image/pgn"})

    return res


def get_game(mlb_id, season, new_only=False):

    if not new_only:
        obj = s3.list_objects('mlb/files/%s/%s.json' % (
            season,
            mlb_id,
        ))

        if 'Contents' in obj:
            r = s3.get_object('mlb/files/%s/%s.json' % (
                season,
                mlb_id,
            )
            )
            mlb_res = json.loads(r['Body'].read())
            return mlb_res

    game_url = MLB_GAME_URL % mlb_id
    mlb_res = requests.get(game_url).json()

    f = open('/tmp/%s.json' % mlb_id, 'w')
    f.write(json.dumps(mlb_res))
    f.close()

    s3.upload_to_s3(
        '/tmp/%s.json' % mlb_id,
        'mlb/files/%s/%s.json' % (season, mlb_id)
    )

    return mlb_res
