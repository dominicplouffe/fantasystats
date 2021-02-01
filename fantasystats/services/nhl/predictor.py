import numpy as np
from fantasystats.context import db  # noqa
from fantasystats.services import search
from fantasystats.services.nhl import features, models, predictor
from datetime import datetime
import requests


def predict(features, clf):
    x = np.array(
        [
            float(_ if len(str(_)) > 0 else 0)
            for _ in features
        ]
    )

    x = x.reshape(1, -1)

    try:
        p = clf.predict(x)[0]
    except ValueError:
        return 0

    return p


def predict_game(away_team_name, home_team_name, game_date):
    away_team_name = search.get_search_value(away_team_name)
    home_team_name = search.get_search_value(home_team_name)

    models.init_models()

    f = features.get_game_features(away_team_name, home_team_name, game_date)
    if f is None:
        return

    away_score = predictor.predict(f['features_away'], models.MODEL)
    home_score = predictor.predict(f['features_home'], models.MODEL)

    # if abs(home_score - away_score) >= 1:
    #     t = away_score
    #     away_score = home_score
    #     home_score = t

    return {
        'home_score': home_score,
        'away_score': away_score
    }


if __name__ == '__main__':

    date = datetime(2021, 1, 28)

    url = 'https://api.bettingnews.com/nhl/games/date/%s' % (
        date.strftime('%Y-%m-%d')
    )

    games = requests.get(url).json()

    num_games = 0
    wins = 0
    for game in games['data']:

        away_team = game['away_team']['team_id']
        home_team = game['home_team']['team_id']

        # sites = game['predictions']['sites']
        # try:
        #     site = [s for s in sites if s['provider'] == 'dratings'][0]
        # except IndexError:
        #     continue

        # scores = {
        #     'home_score': float(site['predictions']['home']['score']),
        #     'away_score': float(site['predictions']['away']['score']),
        # }

        # if scores['home_score'] == scores['away_score']:
        #     continue

        scores = predict_game(
            away_team,
            home_team,
            date
        )

        winner = away_team
        pick = away_team
        if game['team_scoring']['home']['goals'] > game['team_scoring']['away']['goals']:
            winner = home_team

        if scores['home_score'] > scores['away_score']:
            pick = home_team

        num_games += 1
        if winner == pick:
            wins += 1

        win_per = float(wins / num_games)

        print('%s\t%s\t%s\t%s\t%s\t%.1f\t%.1f\t%s\t%s\t%s\t%.2f' % (
            away_team.ljust(30),
            home_team.ljust(30),
            game['team_scoring']['away']['goals'],
            game['team_scoring']['home']['goals'],
            winner.ljust(30),
            scores['away_score'],
            scores['home_score'],
            pick.ljust(30),
            num_games,
            wins,
            win_per
        ))
