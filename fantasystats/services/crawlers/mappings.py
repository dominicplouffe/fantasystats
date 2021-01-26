import pytz
from datetime import datetime
from fantasystats.services import search


NBA_MAPPING = {
    'SA': 'SAS',
    'NY': 'NYK',
    'NO': 'NOP',
    'PHO': 'PHX',
    'GS': 'GSW'
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
