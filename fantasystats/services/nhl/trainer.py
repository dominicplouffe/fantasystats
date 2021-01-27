from fantasystats.context import db, logger
from fantasystats.managers.nhl import game
from fantasystats.services.nhl import models, features
from datetime import datetime, timedelta
from sklearn.svm import SVR


def train():

    start_date = datetime(2016, 10, 1)
    end_date = datetime(2021, 1, 25)

    game_date = start_date

    X = []
    Y = []
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

            Y.append(feature_details['result_home'])
            Y.append(feature_details['result_away'])

        game_date += timedelta(days=1)

    logger.info('training,%s' % len(X))
    reg = SVR(C=1.0, epsilon=0.1, cache_size=1000)
    reg.fit(X, Y)
    models.save_model(reg)


if __name__ == '__main__':
    train()
