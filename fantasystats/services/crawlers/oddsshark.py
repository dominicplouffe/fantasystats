import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.services import search
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nhl import team as nhl_team

URLS = {
    'nba': 'https://www.oddsshark.com/nba/computer-picks',
    'nhl': 'https://www.oddsshark.com/nhl/computer-picks'
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
    'SJ': 'SJS'
}


def get_predictions(league, league_mgr, mappings):

    games = []

    content = requests.get(URLS[league]).content.decode('utf-8')
    doc = html.fromstring(content)

    for card in doc.xpath('//div[@class="picks-card-container"]'):

        abbrs = card.xpath('.//thead/tr/td/span/text()')

        away_abbr = abbrs[2].strip()
        home_abbr = abbrs[4].strip()

        try:
            away_score = float(card.xpath('.//tbody[1]/tr[1]/td[2]/text()')[0])
        except ValueError:
            away_score = 0.00

        try:
            home_score = float(card.xpath('.//tbody[1]/tr[1]/td[3]/text()')[0])
        except ValueError:
            home_score = 0.00

        away_team = league_mgr.get_team_by_abbr(
            mappings.get(away_abbr, away_abbr)
        )[0]
        home_team = league_mgr.get_team_by_abbr(
            mappings.get(home_abbr, home_abbr)
        )[0]

        games.append(
            {
                'game_key': _create_game_key(away_team, home_team),
                'predictions': {
                    'away': {
                        'team': away_team.name_search,
                        'score': away_score
                    },
                    'home': {
                        'team': home_team.name_search,
                        'score': home_score
                    }
                }
            }
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

    nba_games = get_predictions('nba', nba_team, NBA_MAPPING)
    nhl_games = get_predictions('nhl', nhl_team, NHL_MAPPING)

    print(nba_games)
    print(nhl_games)
