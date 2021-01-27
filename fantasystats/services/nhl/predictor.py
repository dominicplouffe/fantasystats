import numpy as np
from fantasystats.context import db  # noqa
from fantasystats.services import search
from fantasystats.services.nhl import features, models, predictor
from datetime import datetime


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

    away_team = predictor.predict(f['features_away'], models.MODEL)
    home_team = predictor.predict(f['features_home'], models.MODEL)

    return {
        'away_team': away_team,
        'home_team': home_team
    }


if __name__ == '__main__':

    print(predict_game(
        'dallas_stars',
        'calgary_flames',
        datetime(2020, 8, 20)
    ))
