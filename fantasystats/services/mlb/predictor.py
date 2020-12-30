import numpy as np
from fantasystats.context import db  # noqa
from fantasystats.services import search
from fantasystats.services.mlb import features, models, predictor


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

    results = {
        'A': None,
        'B': None,
        'C': None,
        'D': None,
        'E': None
    }

    for y in results.keys():
        away_team = predictor.predict(f['features_away'], models.MODELS[y])
        home_team = predictor.predict(f['features_home'], models.MODELS[y])

        away_per = away_team / (home_team + away_team)
        home_per = home_team / (home_team + away_team)

        # optimize_per = 0
        diff = abs(away_per - home_per)
        # cnt = 0
        # while optimize_per == 0:
        #     res = list(db.mlb_optimizer.find(
        #         {'y': y,
        #          'threshold': {'$gte': diff - 0.01}
        #          }).sort([('theshold', 1)]))

        #     cnt += 1
        #     if cnt == 100:
        #         break
        #     if len(res) == 0:
        #         continue

        #     optimize_per = res[0]['per']

        # if away_per > home_per:
        #     away_per = optimize_per
        #     home_per = 1.0 - away_per
        # else:
        #     home_per = optimize_per
        #     away_per = 1.0 - home_per

        results[y] = {
            'home': home_per,
            'away': away_per,
            'diff': diff}

    # majority_count = defaultdict(int)
    # for _, v in results.items():
    #     if v['home'] > v['away']:
    #         majority_count['home'] += 1
    #     else:
    #         majority_count['away'] += 1

    # majority_side = 'home'
    # if majority_count['away'] > majority_count['home']:
    #     majority_side = 'away'

    # predictions = results['A']
    # for k, v in results.items():
    #     if k == 'A':
    #         continue
    #     if v[majority_side] > predictions[majority_side]:
    #         predictions = v

    return {
        away_team_name: results['B']['away'],
        home_team_name: results['C']['home']
    }
