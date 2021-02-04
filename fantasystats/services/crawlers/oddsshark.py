import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nhl import team as nhl_team
from fantasystats.managers.nba import prediction as nba_prediction
from fantasystats.managers.nhl import prediction as nhl_prediction
from fantasystats.services.crawlers.mappings import (
    NBA_MAPPING, NHL_MAPPING, create_game_key
)

URLS = {
    'nba': 'https://www.oddsshark.com/nba/computer-picks',
    'nhl': 'https://www.oddsshark.com/nhl/computer-picks'
}

PROVIDER = 'oddsshark'


def get_predictions(league, league_mgr, pred_mgr, mappings):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

    games = []

    content = requests.get(URLS[league]).content.decode('utf-8')
    doc = html.fromstring(content)

    for card in doc.xpath('//div[@class="picks-card-container"]'):

        abbrs = card.xpath('.//thead/tr/td/span/text()')

        away_abbr = abbrs[2].strip()
        home_abbr = abbrs[4].strip()

        try:
            away_score = float(card.xpath('.//tbody[1]/tr[1]/td[2]/text()')[0])
        except ValueError:
            away_score = 0.00

        try:
            home_score = float(card.xpath('.//tbody[1]/tr[1]/td[3]/text()')[0])
        except ValueError:
            home_score = 0.00

        game_url = card.xpath('.//thead[1]/tr[1]/td[1]/span/a/@href')[0]
        game_url = 'https://www.oddsshark.com%s' % game_url

        context.logger.info(game_url)

        away_team = league_mgr.get_team_by_abbr(
            mappings.get(away_abbr, away_abbr)
        )[0]
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
