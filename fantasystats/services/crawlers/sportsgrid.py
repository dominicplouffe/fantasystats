import pytz
import requests
from lxml import html
from datetime import datetime
from fantasystats import context
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nba import prediction as nba_prediction
from fantasystats.services.crawlers.mappings import (
    NBA_MAPPING, create_game_key
)

URLS = {
    'nba': 'https://www.sportsgrid.com/wp-content/plugins/betting-odds/templates/betting_nba_data.php',
}

PROVIDER = 'sportsgrid'


def get_predictions(league, league_mgr, pred_mgr, mappings):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

    games = []

    games = requests.get(URLS[league]).json()

    for game in games:

        if 'model' not in game:
            continue
        try:
            away_abbr = game['away']['team']
            home_abbr = game['home']['team']

            spread = game['spread']
            total = game['total']

            away_per = float(
                game['model']['awayTeam']['winPercent'].replace('%', '')
            )
            home_per = float(
                game['model']['homeTeam']['winPercent'].replace('%', '')
            )

            away_diff = spread * (away_per / 100)
            home_diff = spread * (home_per / 100)

            if home_per > away_per:
                away_score = round(total - away_diff, 0)
                home_score = round(total + home_diff, 0)
            else:
                away_score = round(total + away_diff, 0)
                home_score = round(total - home_diff, 0)
        except TypeError:
            continue

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
                'game_url': 'https://www.sportsgrid.com/nba/betting/model-picks/',
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
