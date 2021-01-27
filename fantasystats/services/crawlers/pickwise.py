import re
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

from pprint import pprint

URLS = {
    'nba': 'https://www.pickswise.com/sports/nba/',
    'nhl': 'https://www.pickswise.com/sports/nhl/',
}

STATSINSIDER_URL = 'https://levy.statsinsider.com.au/round/matches?Sport=%s' \
    '&Round=%s&Season=2020'
STATS = {}

PROVIDER = 'pickwise'

NHL_START_SEASON = datetime(2021, 1, 14)


def get_game_prediction(url, league, league_mgr, pred_mgr, mappings):

    content = requests.get(url).content.decode('utf-8')
    doc = html.fromstring(content)

    if league == 'nba':
        match_info = re.findall('matchID: "([^"]+)"', content)[0].split('_')
        away_abbr = match_info[4]
        home_abbr = match_info[3]
        week = match_info[2]
    elif league == 'nhl':
        matchup = doc.xpath(
            '//button[@data-component="AnalyticsEvent"]/'
            '@data-analytics-event-label'
        )[0]

        away_info = matchup.split('@')[0].strip()
        home_info = matchup.split('@')[1].strip()
        away_abbr = away_info.split(' ')[0].strip()
        home_abbr = home_info.split(' ')[0].strip()

        diff = datetime.utcnow() - NHL_START_SEASON
        week = diff.days

    stats = _get_stats(week, league)

    away_score = 0
    home_score = 0
    away_per = 0.50
    home_per = 0.50

    for s in stats:
        if (
            s['MatchData']['AwayTeam']['Abv'] == away_abbr
        ) and (
            s['MatchData']['HomeTeam']['Abv'] == home_abbr
        ):
            away_score = round(s['PreData']['PredAwayScore'], 1)
            home_score = round(s['PreData']['PredHomeScore'], 1)

            away_per = round(s['PreData']['PythagAway'], 2)
            home_per = round(1.0 - away_per, 2)

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

    content = requests.get(url).content.decode('utf-8')
    doc = html.fromstring(content)

    for game_url in doc.xpath('//a[@class="CondensedPreview__start"]/@href'):
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

    global STATS

    if week in STATS:
        diff = datetime.now(pytz.UTC) - STATS[week]['date']

        if diff.total_seconds() < 3600:
            return STATS[week]['data']

    data = requests.get(STATSINSIDER_URL % (league.upper(), week)).json()

    STATS[week] = {
        'date': datetime.now(pytz.UTC),
        'data': data
    }

    return data


if __name__ == '__main__':

    print(get_predictions('nba', nba_team, nba_prediction, NBA_MAPPING))
    get_predictions('nhl', nhl_team, nhl_prediction, NHL_MAPPING)