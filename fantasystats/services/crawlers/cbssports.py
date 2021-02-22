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
from fantasystats.services.crawlers.mappings import create_game_key, NHL_MAPPING

NBA_URL = 'https://www.cbssports.com/nba/expert-picks/'
NHL_URL = 'https://www.cbssports.com/nhl/expert-picks/'
MLB_URL = 'https://www.cbssports.com/nhl/expert-picks/'


URLS = {
    'nba': NBA_URL,
    'nhl': NHL_URL,
    'mlb': MLB_URL
}

PROVIDER = 'cbssports'

MLB_MAPPING = {}


def get_predictions(league, league_mgr, pred_mgr, mapping):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

    games = []

    content = requests.get(URLS[league]).content.decode('utf-8')
    doc = html.fromstring(content)

    rows = doc.xpath('//div[@class="picks-tr"]')

    for row in rows:
        teams_cell = row.xpath('./div[1]')
        picks_cell = row.xpath('./div[3]')

        teams = row.xpath('.//span[@class="team"]/a/@href')
        if not teams:
            continue

        if len(teams) != 2:
            continue

        away_team_name = teams[0].split('/')[-2]
        home_team_name = teams[1].split('/')[-2]

        away_team = league_mgr.get_team_by_name(away_team_name)
        home_team = league_mgr.get_team_by_name(home_team_name)

        if away_team is None or home_team is None:
            context.logger.info('CBS cannot find team: %s' % league)
            continue

        spread = row.xpath('.//div[contains(@class, "expert-spread")]/text()')
        if not spread:
            context.logger.info('CBS cannot find spread: %s' % league)
            continue

        if league == 'nhl':
            try:
                spread_team = mapping.get(
                    spread[1].split('\n')[1].strip().upper(),
                    spread[1].split('\n')[1].strip().upper()
                )
                spread_points = float(spread[1].split('\n')[2].strip())

                if spread_points < 0:
                    spread_points = 2
                else:
                    spread_points = -2

            except ValueError:
                context.logger.info(
                    'CBS cannot spread value error: %s' % league
                )
                continue
            except IndexError:
                context.logger.info(
                    'CBS cannot spread index error: %s' % league
                )
                continue
        else:
            spread = row.xpath('.//div[@class="expert-spread"]/text()')
            if not spread:
                context.logger.info('CBS cannot find spread: %s' % league)
                continue

            try:
                spread_team = mapping.get(
                    spread[1].split('\n')[1].strip().upper(),
                    spread[1].split('\n')[1].strip().upper()
                )
                spread_points = float(spread[1].split('\n')[2].strip())

                spread_points = spread_points * -1
            except ValueError:
                context.logger.info(
                    'CBS cannot spread value error: %s' % league
                )
                continue
            except IndexError:
                context.logger.info(
                    'CBS cannot spread index error: %s' % league
                )
                continue

        winning_team = None
        points_to = None
        points_to_give = 0
        if away_team.abbr.lower() == spread_team.lower():
            winning_team = away_team
            if spread_points < 0:
                points_to = home_team
                points_to_give = abs(round(spread_points + 0.5, 0)) - 1
            else:
                points_to = away_team
                points_to_give = round(spread_points + 1.0, 0)
        elif home_team.abbr.lower() == spread_team.lower():
            winning_team = home_team
            if spread_points < 0:
                points_to = away_team
                points_to_give = abs(round(spread_points + 0.5, 0)) - 1
            else:
                points_to = home_team
                points_to_give = round(spread_points + 1.0, 0)
        else:
            context.logger.info('CBS Abbr mismatch: %s - %s' % (
                league, spread_team.lower()
            ))

            continue

        over_under_points = row.xpath('.//div[@class="expert-ou"]/text()')
        over_under_side = row.xpath(
            './/div[@class="expert-picks-col"]//'
            'span[contains(@class, "pick-")]/text()'
        )

        try:
            over_under_points = float(over_under_points[1].strip())
        except ValueError:
            context.logger.info('CBS cannot O/U value error: %s' % league)
            continue
        except IndexError:
            context.logger.info('CBS cannot O/U index error: %s' % league)
            continue

        try:
            over_under_side = over_under_side[0]
        except IndexError:
            context.logger.info('CBS cannot O/U side index error: %s' % league)
            continue

        home_score, away_score = get_score(
            over_under_points,
            over_under_side,
            home_team,
            away_team,
            points_to,
            points_to_give
        )

        games.append(
            {
                'game_key': create_game_key(away_team, home_team),
                'winner': winning_team.name_search,
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


def get_score(
    over_under_points,
    over_under_side,
    home_team,
    away_team,
    points_to,
    points_to_give
):
    home_score = 0
    away_score = 0

    total_score = over_under_points
    if over_under_side == "U":
        total_score = total_score - 1.0
    else:
        total_score = total_score + 1.0

    if points_to.abbr == home_team.abbr:
        home_score += points_to_give
        total_score -= points_to_give
    else:
        away_score += points_to_give
        total_score -= points_to_give

    remaining_points = total_score / 2.0
    home_score += remaining_points
    away_score += remaining_points

    if home_score < 1:
        home_score = 1.0
    if away_score < 1:
        away_score = 1.0

    return home_score, away_score


if __name__ == '__main__':
    get_predictions('nba', nba_team, nba_prediction, NBA_MAPPING)
    get_predictions('nhl', nhl_team, nhl_prediction, NHL_MAPPING)
    get_predictions('mlb', mlb_team, mlb_prediction, MLB_MAPPING)
