import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.mlb import team as mlb_team
from fantasystats.managers.nba import prediction as nba_prediction
from fantasystats.managers.mlb import prediction as mlb_prediction
from fantasystats.services.crawlers.mappings import (
    NBA_MAPPING, create_game_key, MLB_MAPPING
)

URLS = {
    'nba': 'https://www.nbagamesim.com/nba-predictions.asp',
    'mlb': 'https://www.mlbgamesim.com/mlb-predictions.asp'
}

PROVIDER = 'nbagamesim'

MAPPINGS = {
    'Los Angeles Clippers': 'la_clippers'
}


def get_predictions(league, league_mgr, pred_mgr, mappings):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

    games = []

    content = requests.get(URLS[league]).content.decode('utf-8')
    doc = html.fromstring(content)

    for card in doc.xpath('//div[@class="table-responsive"]/table/tr'):
        names = card.xpath('.//td[2]/a/text()')

        away_name = names[0]
        home_name = names[1]

        away_team = league_mgr.get_team_by_name(
            MAPPINGS.get(away_name, away_name)
        )
        home_team = league_mgr.get_team_by_name(
            MAPPINGS.get(home_name, home_name)
        )

        pred_text = card.xpath('.//td[3]/text()')[0]

        win_team = pred_text.split(' win ')[0].strip()
        scores = pred_text.split(' win ')[1].split('-')
        if win_team == away_name:
            away_score = float(scores[0].strip())
            home_score = float(scores[1].strip())
        else:
            away_score = float(scores[1].strip())
            home_score = float(scores[0].strip())

        winner = away_team.name_search
        if home_score > away_score:
            winner = home_team.name_search

        games.append(
            {
                'game_key': create_game_key(away_team, home_team),
                'winner': winner,
                'game_url': 'https://www.nbagamesim.com/nba-predictions.asp',
                'away_team': away_team.name_search,
                'home_team': home_team.name_search,
                'predictions': {
                    'away': {
                        'score': away_score
                    },
                    'home': {
                        'score': home_score
                    }
                }
            }
        )

    for g in games:
        print(g['game_key'])
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
    mlb_games = get_predictions('mlb', mlb_team, mlb_prediction, MLB_MAPPING)
