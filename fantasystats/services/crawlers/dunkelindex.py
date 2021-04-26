import pytz
import requests
from lxml import html
from datetime import datetime, timedelta
from fantasystats import context
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nhl import team as nhl_team
from fantasystats.managers.mlb import team as mlb_team
from fantasystats.managers.nba import prediction as nba_prediction
from fantasystats.managers.nhl import prediction as nhl_prediction
from fantasystats.managers.mlb import prediction as mlb_prediction
from fantasystats.services.crawlers.mappings import (
    NBA_MAPPING, NHL_MAPPING, create_game_key, MLB_MAPPING
)

URLS = {
    'nba': 'https://www.dunkelindex.com/picks/view/basketball/nba',
    'mlb': 'https://www.dunkelindex.com/picks/view/baseball/mlb',
    'nhl': 'https://www.dunkelindex.com/picks/view/hockey/nhl'
}

PROVIDER = 'dunkelindex'

MAPPINGS = {
    'Los Angeles Clippers': 'la_clippers'
}


def get_predictions(league, league_mgr, pred_mgr, mappings):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)
    games = []

    content = requests.get(URLS[league]).content.decode('utf-8')
    doc = html.fromstring(content)

    for card in doc.xpath('.//li[@class="game"]'):

        away_team = card.xpath('.//div[contains(@class, "team-1")]')[0]
        home_team = card.xpath('.//div[contains(@class, "team-2")]')[0]

        away_name = away_team.xpath('.//div/div/p/text()')[0]
        home_name = home_team.xpath('.//div/div/p/text()')[0]

        win_team_score = away_score = float(
            card.xpath(
                './/div[contains(@class, "match-height")]//p[@class="total"]/text()'
            )[0].replace('Total Score: ', '')
        )
        win_team_margin = away_score = float(
            card.xpath(
                './/div[contains(@class, "match-height")]//p[@class="margin"]/text()'
            )[0].replace('Winning Margin: ', '')
        )
        win_team_text = card.xpath(
            './/div[contains(@class, "match-height")]/div/p[1]/text()'
        )[0]

        if win_team_text in away_name:
            away_score = (win_team_score / 2) + (win_team_margin / 2)
            home_score = (win_team_score / 2) - (win_team_margin / 2)

            if away_score == home_score:
                away_score += 1
        else:
            away_score = (win_team_score / 2) - (win_team_margin / 2)
            home_score = (win_team_score / 2) + (win_team_margin / 2)

            if away_score == home_score:
                home_score += 1

        away_team = league_mgr.get_team_by_name(
            MAPPINGS.get(away_name, away_name))
        home_team = league_mgr.get_team_by_name(
            MAPPINGS.get(home_name, home_name))

        winner = away_team.name_search
        if home_score > away_score:
            winner = home_team.name_search

        games.append(
            {
                'game_key': create_game_key(away_team, home_team),
                'winner': winner,
                'game_url': URLS[league],
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
    nhl_games = get_predictions('nhl', nhl_team, nhl_prediction, NHL_MAPPING)
