import requests
from fantasystats import context
from lxml import html
from datetime import datetime, timedelta
from fantasystats.managers.mlb import team as mlb_team
from fantasystats.managers.mlb import game as mlb_game
from fantasystats.managers.nhl import team as nhl_team
from fantasystats.managers.nhl import game as nhl_game

MAPPING = {
    'mlb': {
        'CHW': 'CWS'
    },
    'nhl': {
        'NAS': 'NSH',
        'TB': 'TBL',
        'MON': 'MTL',
        'WAS': 'WSH',
        'VEG': 'VGK'
    }
}

DB_MAP = {
    'nhl': {
        'odds': 'nhl_odds',
        'game': nhl_game,
        'team': nhl_team
    },
    'mlb': {
        'odds': 'mlb_odds',
        'game': mlb_game,
        'team': mlb_team
    },
}


def get_odds(league):

    if league not in ['mlb', 'nhl']:
        raise ValueError('Invalid league')

    date = datetime.utcnow() - timedelta(hours=5)
    r = requests.get('https://rotogrinders.com/%s/odds' % league)

    if r.status_code != 200:
        raise requests.exceptions.RequestException(
            'rotogrinder,blocking,%s' % (
                r.status_code
            )
        )

    doc = html.fromstring(r.content)

    found_games = _get_games(doc, date, league)
    sportsbooks = _get_odds(doc, league)

    book_names = sportsbooks.keys()

    games = [
        {'game_key': g.game_key, '_id': g.game_key} for g in found_games
    ]

    for book in book_names:
        for g in games:
            g[book] = {}

    for book, values in sportsbooks.items():
        for i, odds in enumerate(values):
            games[i][book] = odds

    for g in games:
        context.db[DB_MAP[league]['odds']].replace_one(
            {'_id': g['_id']}, g, upsert=True
        )


def _get_odds(doc, league):
    content_rows = doc.xpath(
        '//div[@data-sport="%s"]/div[@class="scroll-wrapper"]'
        '/div[@class="sportsbook-content"]' % league
    )

    sportsbooks = {}

    for content in content_rows:
        header_row = content.xpath('./div[@class="tbl-hdr-row"]')[0]
        sportsbook = header_row.xpath('.//img/@alt')[0]
        sportsbooks[sportsbook] = []

        team_rows = content.xpath(
            './div[@class="tbl-body"]/div[contains(@class, "row")]'
        )

        team_row = {}
        for row in team_rows:
            row_type = row.xpath('./@data-type')[0]
            values = [x.strip() for x in row.xpath('.//span/text()')]
            if row_type == 'moneyline':
                team_row['money_line'] = {
                    'away': {'odds': values[0]},
                    'home': {'odds': values[1]}
                }
            elif row_type == 'spread':
                team_row['spread'] = {
                    'away': {
                        'spread': '0',
                        'odds': '0'
                    },
                    'home': {
                        'spread': '0',
                        'odds': '0'
                    },
                }

                if values[0] != 'n/a':
                    team_row['spread'] = {
                        'away': {'spread': values[0], 'odds': values[1]},
                        'home': {'spread': values[2], 'odds': values[3]},
                    }
            elif row_type == 'total':
                team_row['over_under'] = {
                    'over': {
                        'points': '0',
                        'odds': '0'
                    },
                    'under': {
                        'points': '0',
                        'odds': '0'
                    },
                }

                if values[0] != 'n/a':
                    team_row['over_under'] = {
                        'over': {
                            'points': values[0].replace('o', ''),
                            'odds': values[1]
                        },
                        'under': {
                            'points': values[2].replace('u', ''),
                            'odds': values[3]
                        },
                    }

            if len(team_row) == 3:
                if team_row['money_line']['away']['odds'] != 'n/a':
                    sportsbooks[sportsbook].append(team_row)
                team_row = {}

    return sportsbooks


def _get_games(doc, date, league):
    games = DB_MAP[league]['game'].get_by_game_date(date)
    found_games = []

    team_rows = doc.xpath(
        '//div[@data-sport="%s"]/div[@class="static-content"]'
        '/div[@class="tbl-body"]/div[contains(@class, "row")]' % league
    )

    for row in team_rows:
        home = row.xpath('./@data-team-home')[0]
        away = row.xpath('./@data-team-away')[0]

        home_team = DB_MAP[league]['team'].get_team_by_abbr(
            MAPPING[league].get(home, home)
        )
        away_team = DB_MAP[league]['team'].get_team_by_abbr(
            MAPPING[league].get(away, away)
        )

        if not home_team or not away_team:
            context.logger.info(
                'cannot find a team,home:%s,away:%s' % (home, away)
            )
            continue
        print(home, away)
        for g in games:
            if (g.home_team == home_team.name_search) and (
                    g.away_team == away_team.name_search
            ):
                found_games.append(g)
                break

    return found_games


if __name__ == '__main__':

    get_odds('mlb')
    get_odds('nhl')
