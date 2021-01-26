import pytz
import requests
from lxml import html
from fantasystats import context
from fantasystats.services import search
from fantasystats.managers.nba import team as nba_team
from fantasystats.managers.nhl import team as nhl_team
from datetime import datetime


URL = 'https://www.scoresandstats.com/previews/basketball/%s/'


def get_predictions(league, league_mgr):

    games = []

    url = URL % league.upper()

    content = requests.get(url).content.decode('utf-8')
    doc = html.fromstring(content)

    boxes = doc.xpath('//article[contains(@class, "pug-single")]')
    for box in boxes:

        between = box.xpath('./section/div[contains(@class, "between")]')

        team_names = between[0]
        away_name = team_names.xpath('./h2/a/text()')[0]
        home_name = team_names.xpath('./h2/a/text()')[1]

        predictions = between[4]
        away_pred = predictions.xpath('./div/b/text()')[0]
        home_pred = predictions.xpath('./div/b/text()')[1]

        print(away_name)
        print(home_name)

        away_team = league_mgr.get_team_by_shortname(away_name)
        home_team = league_mgr.get_team_by_shortname(home_name)

        games.append(
            {
                'game_key': _create_game_key(away_team, home_team),
                'predictions': {
                    'away': {
                        'team': away_team.name_search,
                        'score': away_pred
                    },
                    'home': {
                        'team': home_team.name_search,
                        'score': home_pred
                    }
                }
            }
        )

    return games


def _create_game_key(away_team, home_team):

    d = datetime.now(pytz.UTC)

    return search.create_game_key(
        d,
        away_team,
        home_team,
        'N',
        '1'
    )


if __name__ == '__main__':

    nba_games = get_predictions('NBA', nba_team)
    nhl_games = get_predictions('NHL', nhl_team)
