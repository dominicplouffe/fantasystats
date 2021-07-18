import json
import requests
from fantasystats.context import logger
from datetime import datetime, timedelta
from fantasystats.managers.esports import matches
from fantasystats.services import search


URL = 'https://odds.data.bet/affiliates/tbCiYC2r-0jMRejP5vDizQ/json'


def get_odds():
    try:
        j = requests.get(URL).json()
    except json.decoder.JSONDecodeError:
        logger.info('JSON Error getting URL')
        return

    for e in j['Sport']['eSports']['Events']:

        event_name = e['Name']
        event_id = e['ID']
        category = e['CategoryID']

        for m in e['Matches']:
            match_name = m['Name']
            match_id = e['ID']
            start_time = _parse_start_time(m)

            game_date = datetime(
                start_time.year,
                start_time.month,
                start_time.day
            )

            competitors = {}
            for c in m['Competitors']:
                team_key = search.get_esport_team_key(c['Name'])
                competitors[team_key] = {
                    'name': c['Name'],
                    'logo': c['Logo'],
                    'id': c['ID'],
                    'team_key': team_key
                }

            bets = m['Bets']

            score = m.get('Score', '0:0')

            matches.insert_match(
                game_date,
                start_time,
                match_name,
                match_id,
                event_name,
                event_id,
                category,
                competitors,
                score,
                bets
            )


def _parse_start_time(m):
    if '+' not in m['StartDate']:
        m['StartDate'] = '%s+00:00' % (
            m['StartDate']
        )
    start_time = datetime.strptime(
        m['StartDate'].split('+')[0],
        '%Y-%m-%dT%H:%M:%S'
    )

    offset = int(m['StartDate'].split('+')[1].split(':')[0])
    start_time -= timedelta(hours=offset)

    return start_time


if __name__ == '__main__':
    get_odds()
