import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.services import search
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nhl import team as nhl_team

NBA_URL = 'https://www.dratings.com/predictor/nba-basketball-predictions/'
NHL_URL = 'https://www.dratings.com/predictor/nhl-hockey-predictions/'

NBA_MAPPING = {
    'Los Angeles Clippers': 'LA Clippers'
}
NHL_MAPPING = {}

SCORES_IDX = {
    'nba': 5,
    'nhl': 6
}

URLS = {
    'nba': NBA_URL,
    'nhl': NHL_URL
}


def get_predictions(league, league_mgr, mapping):

    games = []

    content = requests.get(URLS[league]).content.decode('utf-8')
    doc = html.fromstring(content)

    games_rows = doc.xpath(
        '//h2[contains(text(), "Upcoming Games")]/../table//tbody/tr'
    )

    for row in games_rows:
        names = row.xpath('./td[2]/span/a/text()')
        away_name = names[0]
        home_name = names[1]

        pers = row.xpath('./td[3]/span/text()')

        try:
            away_per = float(pers[0].replace('%', ''))
        except ValueError:
            away_per = 0.00

        try:
            home_per = float(pers[1].replace('%', ''))
        except ValueError:
            home_per = 0.00

        scores = row.xpath('./td[%s]/text()' % SCORES_IDX[league])
        away_score = float(scores[0])
        home_score = float(scores[1])

        away_team = league_mgr.get_team_by_name(
            mapping.get(away_name, away_name)
        )
        home_team = league_mgr.get_team_by_name(
            mapping.get(home_name, home_name)
        )

        games.append(
            {
                'game_key': _create_game_key(away_team, home_team),
                'predictions': {
                    'away': {
                        'team': away_team.name_search,
                        'score': away_score,
                        'per': away_per
                    },
                    'home': {
                        'team': home_team.name_search,
                        'score': home_score,
                        'per': home_per
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
