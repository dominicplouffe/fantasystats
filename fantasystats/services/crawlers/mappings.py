import pytz
from datetime import datetime
from fantasystats.services import search

HEADERS = {
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/74.0.3729.169 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
    'application/signed-exchange;v=b3',
    'referer': 'https://www.google.com/',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9',
}

NBA_MAPPING = {
    'SA': 'SAS',
    'NY': 'NYK',
    'NO': 'NOP',
    'PHO': 'PHX',
    'GS': 'GSW',
    'CHR': 'CHA',
    'SAN': 'SAS',
    'BK': 'BKN'
}
NHL_MAPPING = {
    'CLB': 'CBJ',
    'NJ': 'NJD',
    'WAS': 'WSH',
    'LA': 'LAK',
    'NAS': 'NSH',
    'CAL': 'CGY',
    'SJ': 'SJS',
    'WIN': 'WPG',
    'VEG': 'VGK',
    'TB': 'TBL',
    'MON': 'MTL'
}


def create_game_key(away_team, home_team):

    d = datetime.now(pytz.UTC)

    return search.create_game_key(
        d,
        away_team,
        home_team,
        'N',
        '1'
    )
