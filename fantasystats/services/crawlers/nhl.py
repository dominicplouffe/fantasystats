import json
import requests
from datetime import datetime, timedelta
from fantasystats.services import search
from fantasystats.tools import s3

PLAYER_IMAGE_URL = 'https://nhl.bamcontent.com/images/headshots/' \
                   'current/168x168/%s.jpg'

SCHEDULE_URL = 'https://statsapi.web.nhl.com/api/v1/schedule?' \
               'startDate=%s&endDate=%s&hydrate=team,linescore,broadcasts(all)' \
               ',tickets,game(content(media(epg)),seriesSummary),' \
               'radioBroadcasts,metadata,seriesSummary(series)' \
               '&site=en_nhlCA&teamId=&gameType=&timecode='

NHL_GAME_URL = 'https://statsapi.web.nhl.com/api/v1/game/%s/feed/live'


def get_player_thumbnail(player_id, player_name):

    res = requests.get(PLAYER_IMAGE_URL % player_id)

    if res.status_code == 200:

        filename = search.get_search_value(player_name)
        f = open('/tmp/%s.png' % filename, 'wb')
        f.write(res.content)
        f.close()

        s3.upload_to_s3(
            '/tmp/%s.png' % filename,
            'nhl/players/%s.png' % filename,
            extra={'ACL': 'public-read', 'ContentType': "image/pgn"}
        )

        return '%s.png' % filename

    return None


def get_schedule():

    start_date = datetime.utcnow() - timedelta(days=1)
    end_date = datetime.utcnow() + timedelta(days=1)
    year = start_date.year
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    nhl_url = SCHEDULE_URL % (
        start_date,
        end_date
    )

    res = requests.get(nhl_url).json()
    filename = 'schedule.json'
    f = open('/tmp/%s.png' % filename, 'w')
    f.write(json.dumps(res))
    f.close()

    s3.upload_to_s3(
        '/tmp/%s.png' % filename,
        'nhl/files/%s/%s.png' % (
            year, filename
        ),
        extra={'ACL': 'public-read', 'ContentType': "image/pgn"}
    )

    return res


def get_game(nhl_id, season, new_only=False):

    if not new_only:
        obj = s3.list_objects('nhl/files/%s/%s.json' % (
            season,
            nhl_id,
        ))

        if 'Contents' in obj:
            r = s3.get_object('nhl/files/%s/%s.json' % (
                season,
                nhl_id,
            )
            )
            nhl_res = json.loads(r['Body'].read())
            return nhl_res

    game_url = NHL_GAME_URL % nhl_id
    nhl_res = requests.get(game_url).json()

    f = open('/tmp/%s.json' % nhl_id, 'w')
    f.write(json.dumps(nhl_res))
    f.close()

    s3.upload_to_s3(
        '/tmp/%s.json' % nhl_id,
        'nhl/files/%s/%s.json' % (season, nhl_id)
    )

    return nhl_res
