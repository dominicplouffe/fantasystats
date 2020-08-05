import requests
import json
import time
import os
from fantasystats.tools import s3

year = '20192020'


def get_schedule():
    f = s3.get_object('nhl/files/schedule-%s.json' % year)

    return json.loads(f['Body'].read())


def save_game(game_id, content):
    f = open('/tmp/%s.json' % game_id, 'w')
    f.write(content)
    f.close()

    s3.upload_to_s3(
        '/tmp/%s.json' % game_id,
        'nhl/files/%s/%s.json' % (year, game_id)
    )


def check_game_exist(game_id):

    files = os.listdir('/tmp')
    if '%s.json' % game_id in files:
        return True

    return False


if __name__ == '__main__':
    schedule = get_schedule()

    for d in schedule['dates']:
        for g in d['games']:
            url = 'https://statsapi.web.nhl.com//{0}'.format(g['link'])
            game_data = requests.get(url).json()
            if 'gamePk' not in game_data:
                print('Error getting game_id: %s' % g['gamePk'])
            else:
                print('Game Id => %s' % g['gamePk'])
                if not check_game_exist(g['gamePk']):
                    save_game(g['gamePk'], json.dumps(game_data))
                    time.sleep(1.0)
