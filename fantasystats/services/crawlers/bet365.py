import xmltodict
import requests
from fantasystats import context
from lxml import html
from datetime import datetime, timedelta
from fantasystats.managers.mlb import team as mlb_team
from fantasystats.managers.mlb import game as mlb_game
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nba import game as nba_game

from fantasystats.services.crawlers.mappings import (
    NBA_MAPPING, NHL_MAPPING, MLB_MAPPING
)

MLB_URL = 'http://oddsfeed2.nj.bet365.com/baseball_v2' \
    '?&EventGroupID=20525425&LanguageID=1'
NBA_URL = 'http://oddsfeed2.nj.bet365.com/basketball_v2' \
    '?&EventGroupID=20604387&LanguageID=1'

MAPPING = {
    'mlb': MLB_MAPPING,
    'nhl': NHL_MAPPING,
    'nba': NBA_MAPPING
}

DB_MAP = {
    # 'nhl': {
    #     'odds': 'nhl_odds',
    #     'odds_history': 'nhl_odds_history',
    #     'game': nhl_game,
    #     'team': nhl_team
    # },
    'mlb': {
        'odds': 'mlb_odds',
        'odds_history': 'mlb_odds_history',
        'game': mlb_game,
        'team': mlb_team,
        'url': MLB_URL
    },
    'nba': {
        'odds': 'nba_odds',
        'odds_history': 'nba_odds_history',
        'game': nba_game,
        'team': nba_team,
        'url': NBA_URL
    },
}


def get_odds(league, db_map):

    if league not in ['mlb', 'nhl', 'nba']:
        raise ValueError('Invalid league')

    date = datetime.utcnow() - timedelta(hours=5)
    r = requests.get(db_map['url'])

    doc = xmltodict.parse(r.content)

    games = DB_MAP[league]['game'].get_by_game_date(date)

    for ev in doc['Sport']['EventGroup']['Event']:
        away = ev['@Name'].split('@')[0].strip().split(' ')[0]
        home = ev['@Name'].split('@')[1].strip().split(' ')[0]

        home, away = translante(home, away, ev['@Name'])

        print(home, away)
        home_team = DB_MAP[league]['team'].get_team_by_abbr(
            MAPPING[league].get(home, home)
        )[0]
        print('found home')
        away_team = DB_MAP[league]['team'].get_team_by_abbr(
            MAPPING[league].get(away, away)
        )[0]
        print('found away')

        if not home_team or not away_team:
            context.logger.info(
                'cannot find a team,home:%s,away:%s' % (home, away)
            )
            continue

        found_game = None
        for g in games:
            if (g.home_team == home_team.name_search) and (
                    g.away_team == away_team.name_search
            ):
                found_game = g
                break

        if not found_game:
            context.logger.info(
                'cannot find game,home:%s,away:%s' % (home, away)
            )
            continue

        team_row = {}
        for mkt in ev['Market']:
            if mkt['@Name'] == 'Money Line':
                if mkt['Participant'][0]['@OddsAmerican'] == 'OFF':
                    team_row = {}
                    break
                team_row['money_line'] = {
                    'away': {'odds': mkt['Participant'][0]['@OddsAmerican']},
                    'home': {'odds': mkt['Participant'][1]['@OddsAmerican']}
                }
            elif mkt['@Name'] in ['Run Line', 'Point Spread']:
                if mkt['Participant'][0]['@OddsAmerican'] == 'OFF':
                    team_row = {}
                    break

                team_row['spread'] = {
                    'away': {
                        'spread': mkt['Participant'][0]['@Handicap'],
                        'odds': mkt['Participant'][0]['@OddsAmerican']
                    },
                    'home': {
                        'spread': mkt['Participant'][1]['@Handicap'],
                        'odds': mkt['Participant'][1]['@OddsAmerican']
                    },
                }
            elif mkt['@Name'] == 'Game Totals':
                if mkt['Participant'][0]['@OddsAmerican'] == 'OFF':
                    team_row = {}
                    break

                team_row['over_under'] = {
                    'over': {
                        'points': mkt['Participant'][0]['@Handicap'],
                        'odds': mkt['Participant'][0]['@OddsAmerican']
                    },
                    'under': {
                        'points': mkt['Participant'][1]['@Handicap'],
                        'odds': mkt['Participant'][1]['@OddsAmerican']
                    },
                }
            else:
                continue

        if not team_row:
            continue
        print(found_game)
        odds = context.db[DB_MAP[league]['odds']].find_one({
            '_id': found_game['game_key']
        })

        if odds:
            for bet_type in ['over_under', 'spread', 'money_line']:
                for k, v in team_row[bet_type].items():
                    if team_row[bet_type][k]['odds'][0] != '-':
                        team_row[bet_type][k]['odds'] = '+%s' % team_row[bet_type][k]['odds']
            odds['Bet365'] = team_row
            context.db[DB_MAP[league]['odds']].replace_one(
                {'_id': odds['_id']}, odds, upsert=False
            )


def translante(home, away, name):
    if home == 'CHI' and 'Cubs' in name:
        home = 'CHC'
    if away == 'CHI' and 'Cubs' in name:
        away = 'CHC'
    if home == 'CHI' and 'White Sox' in name:
        home = 'CWS'
    if away == 'CHI' and 'White Sox' in name:
        away = 'CWS'

    if home == 'NY' and 'Yankees' in name:
        home = 'NYY'
    if away == 'NY' and 'Yankees' in name:
        away = 'NYY'
    if home == 'NY' and 'Mets' in name:
        home = 'NYM'
    if away == 'NY' and 'Mets' in name:
        away = 'NYM'

    if home == 'NY' and 'Islanders' in name:
        home = 'NYI'
    if away == 'NY' and 'Islanders' in name:
        away = 'NYI'
    if home == 'NY' and 'Rangers' in name:
        home = 'NYR'
    if away == 'NY' and 'Rangers' in name:
        away = 'NYR'

    if home == 'LA' and 'Dodgers' in name:
        home = 'LAD'
    if away == 'LA' and 'Dodgers' in name:
        away = 'LAD'
    if home == 'LA' and 'Angels' in name:
        home = 'LAA'
    if away == 'LA' and 'Angels' in name:
        away = 'LAA'

    if home == 'LA' and 'Lakers' in name:
        home = 'LAL'
    if away == 'LA' and 'Lakers' in name:
        away = 'LAL'
    if home == 'LA' and 'Clippers' in name:
        home = 'LAC'
    if away == 'LA' and 'Clippers' in name:
        away = 'LAC'

    return home, away


if __name__ == '__main__':

    for league, db_map in DB_MAP.items():

        get_odds(league, db_map)
