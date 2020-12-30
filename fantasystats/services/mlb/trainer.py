from fantasystats.context import db, logger
from fantasystats.managers.mlb import game
from fantasystats.services.mlb import models, predictor, features
from datetime import datetime, timedelta
from sklearn.svm import SVR


def train():

    start_date = datetime(2017, 3, 1)
    end_date = datetime(2019, 8, 31)

    game_date = start_date

    X = []
    Y = {'A': [], 'B': [], 'C': [], 'D': [], 'E': []}
    while game_date <= end_date:

        logger.info('train features,%s' % game_date)
        games = game.get_by_game_date(game_date)

        for game_info in games:
            feature_details = features.get_game_features(
                game_info.away_team,
                game_info.home_team,
                game_date,
                game_info=game_info
            )
            if not feature_details:
                continue

            X.append(feature_details['features_home'])
            X.append(feature_details['features_away'])

            Y['A'].append(feature_details['result_home']['A'])
            Y['B'].append(feature_details['result_home']['B'])
            Y['C'].append(feature_details['result_home']['C'])
            Y['D'].append(feature_details['result_home']['D'])
            Y['E'].append(feature_details['result_home']['E'])

            Y['A'].append(feature_details['result_away']['A'])
            Y['B'].append(feature_details['result_away']['B'])
            Y['C'].append(feature_details['result_away']['C'])
            Y['D'].append(feature_details['result_away']['D'])
            Y['E'].append(feature_details['result_away']['E'])

        game_date += timedelta(days=1)

    clfs = {}
    for y in ['A', 'B', 'C', 'D', 'E']:
        logger.info('training,%s,%s' % (y, len(X)))
        reg = SVR(C=1.0, epsilon=0.1, cache_size=1000)
        reg.fit(X, Y[y])

        models.save_model(reg, y)
        clfs[y] = models.load_model(y)

        logger.info('optimizing,%s' % y)
        optimize(clfs[y], y)


def optimize(clf, y):
    threshold = 0.00
    for i in range(0, 100):

        date = datetime(2019, 9, 1)
        cnt = 0
        wins = 0
        while date < datetime(2019, 10, 31):
            for g in game.get_by_game_date(date):
                f = features.get_game_features(g.away_team, g.home_team, date)
                if f is None:
                    continue
                away_team = predictor.predict(f['features_away'], clf)
                home_team = predictor.predict(f['features_home'], clf)

                if away_team < 0:
                    away_team = 0.0
                if home_team < 0:
                    home_team = 0.0
                away_per = away_team / (home_team + away_team)
                home_per = home_team / (home_team + away_team)
                if abs(away_per - home_per) < threshold:
                    continue
                if home_team > away_team:
                    chosen_side = 'home'
                else:
                    chosen_side = 'away'
                is_win = 0
                if chosen_side == g.winner_side:
                    is_win += 1
                cnt += 1
                wins += is_win
            date += timedelta(days=1)

        if cnt < 10:
            break

        logger.info('predict,%s,%.2f,%s,%s,%s' % (
            y,
            threshold,
            cnt,
            wins,
            round(wins / cnt, 3)
        ))
        rec = {
            '_id': '%s-%.2f' % (y, threshold),
            'created_on': datetime.utcnow(),
            'threshold': threshold,
            'y': y,
            'cnt': cnt,
            'wins': wins,
            'per': round(wins / cnt, 3)
        }
        db.mlb_optimizer.replace_one({'_id': rec['_id']}, rec, upsert=True)
        threshold += 0.01


if __name__ == '__main__':
    train()
