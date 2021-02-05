import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.services import search
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nba import prediction as nba_prediction
from fantasystats.services.crawlers.mappings import create_game_key

NBA_URL = 'https://www.wunderdog.com/nba-basketball-matchups.html'

NBA_MAPPING = {
    'Los Angeles Clippers': 'LA Clippers'
}
NHL_MAPPING = {}

SCORES_IDX = {
    'nba': 5,
    'nhl': 6
}

URLS = {
    'nba': NBA_URL
}

PROVIDER = 'wunderdog'


def get_predictions(league, league_mgr, pred_mgr, mapping):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

    games = []

    content = requests.get(URLS[league]).content.decode('utf-8')
    doc = html.fromstring(content)

    games_rows = doc.xpath(
        '//table[contains(@class, "matchup_table")]/tbody/tr'
    )

    day_count = 0
    for row in games_rows:
        class_name = row.xpath('./@class')

        if len(class_name) == 0:
            matchup_url = 'https://www.wunderdog.com%s' % (
                row.xpath('./td[3]/a/@href')[0]
            )
            game = get_matchup(league, league_mgr, mapping, matchup_url)
            games.append(game)
        else:
            day_count += 1

            if day_count == 2:
                break

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


def get_matchup(league, league_mgr, mapping, matchup_url):

    content = requests.get(matchup_url).content.decode('utf-8')
    doc = html.fromstring(content)

    details = doc.xpath(
        '//table[contains(@class, "detailed_matchup_table")]'
    )[0]

    away = details.xpath('.//tbody/tr[1]')[0]
    home = details.xpath('.//tbody/tr[2]')[0]

    away_name = away.xpath('./td[1]/text()')[0]
    home_name = home.xpath('./td[1]/text()')[0]

    away_team = league_mgr.get_team_by_name(
        mapping.get(away_name, away_name)
    )
    home_team = league_mgr.get_team_by_name(
        mapping.get(home_name, home_name)
    )

    away_score = float(away.xpath('./td[2]/span/text()')[0])
    home_score = float(home.xpath('./td[2]/span/text()')[0])

    away_per = float(away.xpath(
        './td[3]/div[1]/text()')[0].replace('%', '')) / 100
    home_per = float(home.xpath(
        './td[3]/div[1]/text()')[0].replace('%', '')) / 100

    winner = away_team.name_search
    if home_score > away_score:
        winner = home_team.name_search

    return {
        'game_key': create_game_key(away_team, home_team),
        'winner': winner,
        'game_url': matchup_url,
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


if __name__ == '__main__':

    nba_games = get_predictions('nba', nba_team, nba_prediction, NBA_MAPPING)
