import re
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
from fantasystats.services.crawlers.mappings import (
    NBA_MAPPING, NHL_MAPPING, create_game_key, HEADERS, MLB_MAPPING
)

from pprint import pprint

URLS = {
    'nba': 'https://www.pickswise.com/sports/nba/',
    'nhl': 'https://www.pickswise.com/sports/nhl/',
    'mlb': 'https://www.pickswise.com/sports/mlb/'
}

STATSINSIDER_URL = 'https://levy.statsinsider.com.au/round/matches?Sport=%s' \
    '&Round=%s&Season=%s'
STATS = {}

PROVIDER = 'pickwise'

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


MAPPINGS = {
    'Los Angeles Clippers': 'la_clippers'
}


def get_game_prediction(url, league, league_mgr, pred_mgr, mappings):

    content = requests.get(url, headers=HEADERS).content.decode('utf-8')
    doc = html.fromstring(content)
    if league == 'nba':
        team_names = doc.xpath(
            '//div[@class="FixtureTeams__team-name FixtureTeams__team-name'
            '--desktop"]/text()'
        )
        away_team = league_mgr.get_team_by_name(
            MAPPINGS.get(team_names[0].strip(), team_names[0].strip())
        )
        home_team = league_mgr.get_team_by_name(
            MAPPINGS.get(team_names[1].strip(), team_names[1].strip())
        )

        away_abbr = away_team.abbr
        home_abbr = home_team.abbr

        diff = datetime.utcnow() - START_DATE[league]
        week = diff.days

    elif league == 'nhl':
        team_names = doc.xpath(
            '//div[@class="FixtureTeams__team-name FixtureTeams__team-name--desktop"]/text()')

        away_team = league_mgr.get_team_by_name(team_names[0].strip())
        home_team = league_mgr.get_team_by_name(team_names[1].strip())

        away_abbr = away_team.abbr
        home_abbr = home_team.abbr

        diff = datetime.utcnow() - START_DATE[league]
        week = diff.days

    elif league == 'mlb':
        team_names = doc.xpath(
            '//div[@class="FixtureTeams__team-name FixtureTeams__team-name'
            '--desktop"]/text()'
        )

        away_team = league_mgr.get_team_by_name(team_names[0].strip())
        home_team = league_mgr.get_team_by_name(team_names[1].strip())

        away_abbr = away_team.abbr
        home_abbr = home_team.abbr

        diff = datetime.utcnow() - START_DATE[league]
        week = diff.days

    stats = _get_stats(week, league)

    away_score = 0
    home_score = 0
    away_per = 0.50
    home_per = 0.50

    for s in stats:

        data_away = s['MatchData']['AwayTeam']['Abv']
        data_home = s['MatchData']['HomeTeam']['Abv']

        data_away = mappings.get(data_away, data_away)
        data_home = mappings.get(data_home, data_home)

        if (
            data_away == away_abbr
        ) and (
            data_home == home_abbr
        ):
            away_score = round(s['PreData'].get('PredAwayScore', 0), 1)
            home_score = round(s['PreData'].get('PredHomeScore', 0), 1)

            away_per = round(s['PreData']['PythagAway'], 2)
            home_per = round(1.0 - away_per, 2)

            if away_score == 0:
                away_score = away_per * 10
            if home_score == 0:
                home_score = home_per * 10

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
                'per': away_per
            },
            'home': {
                'score': home_score,
                'per': home_per
            }
        }
    }


def get_predictions(league, league_mgr, pred_mgr, mappings):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

    games = []
    url = URLS[league]

    context.logger.info(url)

    content = requests.get(url).content.decode('utf-8')
    doc = html.fromstring(content)

    for game_url in doc.xpath(
        '//a[@data-analytics-event-category="Pick Prediction Header"]/@href'
    ):
        context.logger.info(game_url)
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


def _get_stats(week, league):

    # global STATS

    # if week in STATS:
    #     diff = datetime.now(pytz.UTC) - STATS[week]['date']

    #     if diff.total_seconds() < 3600:
    #         return STATS[week]['data']

    context.logger.info(STATSINSIDER_URL %
                        (league.upper(), week, YEAR[league]))
    data = requests.get(STATSINSIDER_URL %
                        (league.upper(), week, YEAR[league])).json()

    STATS[week] = {
        'date': datetime.now(pytz.UTC),
        'data': data
    }

    return data


if __name__ == '__main__':

    get_predictions('nba', nba_team, nba_prediction, NBA_MAPPING)
    get_predictions('nhl', nhl_team, nhl_prediction, NHL_MAPPING)
    get_predictions('mlb', mlb_team, mlb_prediction, MLB_MAPPING)
