import requests
from fantasystats.tools import s3
from unidecode import unidecode
from fantasystats.services import search

PLAYER_SEARCH_URL = 'https://typeahead.mlb.com/api/v1/typeahead/suggestions/%s'


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
