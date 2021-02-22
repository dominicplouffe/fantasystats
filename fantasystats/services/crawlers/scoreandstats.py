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


URLS = {
    'nba': 'https://www.scoresandstats.com/previews/basketball/nba/',
    'nhl': 'https://www.scoresandstats.com/previews/hockey/nhl/',
    'mlb': 'https://www.scoresandstats.com/previews/hockey/mlb/'
}

PROVIDER = 'scoresandstats'


def get_predictions(league, league_mgr, pred_mgr):

    game_date = datetime.now(pytz.UTC)
    game_date = datetime(game_date.year, game_date.month, game_date.day)

    games = []

    url = URLS[league.lower()]

    content = requests.get(url).content.decode('utf-8')
    doc = html.fromstring(content)

    boxes = doc.xpath('//article[contains(@class, "pug-single")]')
    for box in boxes:

        between = box.xpath('./section/div[contains(@class, "between")]')

        team_names = between[0]
        away_name = team_names.xpath('./h2/a/text()')[0]
        home_name = team_names.xpath('./h2/a/text()')[1]

        predictions = between[4]
        try:
            away_score = float(predictions.xpath('./div/b/text()')[0])
            home_score = float(predictions.xpath('./div/b/text()')[1])
        except ValueError:
            away_score = 0.00
            home_score = 0.00

        away_team = league_mgr.get_team_by_shortname(away_name)
        home_team = league_mgr.get_team_by_shortname(home_name)

        winner = away_team.name_search
        if home_score > away_score:
            winner = home_team.name_search

        game_url = box.xpath('.//a/@href')[0]
        game_url = 'https://www.scoresandstats.com%s' % game_url

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

    nba_games = get_predictions('NBA', nba_team, nba_prediction)
    nhl_games = get_predictions('NHL', nhl_team, nhl_prediction)
    mlb_games = get_predictions('MLB', mlb_team, mlb_prediction)
