import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.services import search
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nhl import team as nhl_team

URLS = {
    'nba': 'https://www.sportsbettingdime.com/nba/odds/',
    'nhl': 'https://www.sportsbettingdime.com/nhl/odds/',
}
NBA_MAPPING = {
    'NY': 'NYK'
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


def get_game_prediction(url, league, league_mgr, mappings):

    content = requests.get(url).content.decode('utf-8')
    doc = html.fromstring(content)

    data = doc.xpath(
        '//h3[contains(text(), "PREDICTED")]/../../div[2]/div/div/div/text()'
    )

    away_score = float(data[0])
    away_abbr = data[1]
    home_score = float(data[2])
    home_abbr = data[3]

    away_team = league_mgr.get_team_by_abbr(
        mappings.get(away_abbr, away_abbr)
    )[0]
    home_team = league_mgr.get_team_by_abbr(
        mappings.get(home_abbr, home_abbr)
    )[0]

    return {
        'game_key': _create_game_key(away_team, home_team),
        'predictions': {
            'away': {
                'team': away_team.name_search,
                'score': away_score,
            },
            'home': {
                'team': home_team.name_search,
                'score': home_score,
            }
        }
    }


def get_predictions(league, league_mgr, mappings):

    games = []
    url = URLS[league]

    content = requests.get(url).content.decode('utf-8')
    doc = html.fromstring(content)

    for game_url in doc.xpath('//time[contains(text(), "Today")]/../'
                              'table[contains(@class, "odds-table")]'
                              '//a[contains(@href, "/'
                              'odds/")]/@href'
                              ):
        games.append(
            get_game_prediction(game_url, league, league_mgr, mappings)
        )

    return games


def _create_game_key(away_team, home_team):

    d = datetime.now(pytz.UTC)

    return search.create_game_key(
        d,
        away_team,
        home_team,
        'N',
        '1'
    )


if __name__ == '__main__':

    # get_game_prediction(
    #     'https://www.sportsbettingdime.com/nba/odds/2021012712-nba-lac-atl/',
    #     'nba',
    #     nba_team,
    #     NBA_MAPPING
    # )

    print(get_predictions('nba', nba_team, NBA_MAPPING))
    print(get_predictions('nhl', nhl_team, NHL_MAPPING))
