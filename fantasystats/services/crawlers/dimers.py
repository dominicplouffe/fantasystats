import pytz
import requests
from lxml import html
from datetime import datetime
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

START_DATE = {
    'nba': datetime(2020, 12, 21),
    'nhl': datetime(2021, 1, 12),
    'mlb': datetime(2021, 3, 31)
}

YEAR = {
    'nba': '2020',
    'nhl': '2020',
    'mlb': '2021',
}

STATSINSIDER_URL = 'https://levy.statsinsider.com.au/round/matches?Sport=%s' \
    '&Round=%s&Season=%s'
STATS = {}

PROVIDER = 'dimers'


def _get_stats(week, league):

    context.logger.info(STATSINSIDER_URL %
                        (league.upper(), week, YEAR[league]))
    data = requests.get(STATSINSIDER_URL %
                        (league.upper(), week, YEAR[league])).json()

    STATS[week] = {
        'date': datetime.now(pytz.UTC),
        'data': data
    }

    return data


def get_predictions(league, league_mgr, pred_mgr, mappings):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

    games = []

    if league == 'nba':
        diff = datetime.utcnow() - START_DATE[league]
        week = diff.days

    elif league == 'nhl':
        diff = datetime.utcnow() - START_DATE[league]
        week = diff.days

    elif league == 'mlb':
        diff = datetime.utcnow() - START_DATE[league]
        week = diff.days

    stats = _get_stats(week, league)

    for game in stats:
        match = game['MatchData']
        pre_data = game['PreData']

        away_abbr = match['AwayTeam']['Abv']
        home_abbr = match['HomeTeam']['Abv']

        away_score = pre_data['PredAwayScore']
        home_score = pre_data['PredHomeScore']

        game_url = 'https://www.dimers.com/bet-hub/%s/schedule/%s_%s_%s_%s' % (
            league,
            YEAR[league],
            week,
            home_abbr.lower(),
            away_abbr.lower()
        )

        print(game_url)

        away_team = league_mgr.get_team_by_abbr(
            mappings.get(away_abbr, away_abbr)
        )[0]
        context.logger.info('home_abbr: %s' % home_abbr)
        home_team = league_mgr.get_team_by_abbr(
            mappings.get(home_abbr, home_abbr)
        )[0]

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
    nhl_games = get_predictions('nhl', nhl_team, nhl_prediction, NHL_MAPPING)
