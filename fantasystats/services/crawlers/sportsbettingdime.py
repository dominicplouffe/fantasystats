import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.services import search
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nhl import team as nhl_team
from fantasystats.managers.nba import prediction as nba_prediction
from fantasystats.managers.nhl import prediction as nhl_prediction
from fantasystats.services.crawlers.mappings import (
    NBA_MAPPING, NHL_MAPPING, create_game_key
)

URLS = {
    'nba': 'https://www.sportsbettingdime.com/nba/odds/',
    'nhl': 'https://www.sportsbettingdime.com/nhl/odds/',
}

PROVIDER = 'sportsbettingdime'


def get_game_prediction(url, league, league_mgr, pred_mgr, mappings):

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

    winner = away_team.name_search
    if home_score > away_score:
        winner = home_team.name_search

    return {
        'game_key': create_game_key(away_team, home_team),
        'winner': winner,
        'game_url': url,
        'away_team': away_team.name_search,
        'home_team': home_team.name_search,
        'predictions': {
            'away': {
                'score': away_score,
            },
            'home': {
                'score': home_score,
            }
        }
    }


def get_predictions(league, league_mgr, pred_mgr, mappings):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

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
            get_game_prediction(
                game_url, league, league_mgr, pred_mgr, mappings
            )
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

    get_predictions('nba', nba_team, nba_prediction, NBA_MAPPING)
    get_predictions('nhl', nhl_team, nhl_prediction, NHL_MAPPING)
