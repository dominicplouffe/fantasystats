import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.services import search
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nhl import team as nhl_team
from fantasystats.managers.mlb import team as mlb_team
from fantasystats.managers.nba import prediction as nba_prediction
from fantasystats.managers.nhl import prediction as nhl_prediction
from fantasystats.managers.mlb import prediction as mlb_prediction
from fantasystats.services.crawlers.mappings import create_game_key

NBA_URL = 'https://www.dratings.com/predictor/nba-basketball-predictions/'
NHL_URL = 'https://www.dratings.com/predictor/nhl-hockey-predictions/'
MLB_URL = 'https://www.dratings.com/predictor/nhl-hockey-predictions/'

NBA_MAPPING = {
    'Los Angeles Clippers': 'LA Clippers'
}
NHL_MAPPING = {}
MLB_MAPPING = {}

SCORES_IDX = {
    'nba': 5,
    'nhl': 6
}

URLS = {
    'nba': NBA_URL,
    'nhl': NHL_URL
}

PROVIDER = 'dratings'


def get_predictions(league, league_mgr, pred_mgr, mapping):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

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

        game_url = row.xpath('./td[1]/a/@href')[0]
        game_url = 'https://www.dratings.com%s' % game_url

        winner = away_team.name_search
        if home_score > away_score:
            winner = home_team.name_search

        games.append(
            {
                'game_key': create_game_key(away_team, home_team),
                'winner': winner,
                'game_url': game_url,
                'away_team': away_team.name_search,
                'home_team': home_team.name_search,
                'predictions': {
                    'away': {
                        'score': away_score,
                        'per': away_per
                    },
                    'home': {
                        'score': home_score,
                        'per': home_per
                    }
                }
            }
        )

    for g in games:
        pred_mgr.save_prediction(
            g['game_key'],
            game_date,
            g['away_team'],
            g['home_team'],
            g['winner'],
            PROVIDER,
            g['game_url'],
            g['predictions']
        )

    return games


if __name__ == '__main__':

    nba_games = get_predictions('nba', nba_team, nba_prediction, NBA_MAPPING)
    nhl_games = get_predictions('nhl', nhl_team, nhl_prediction, NHL_MAPPING)
    # get_predictions('mlb', mlb_team, mlb_prediction, MLB_MAPPING)
