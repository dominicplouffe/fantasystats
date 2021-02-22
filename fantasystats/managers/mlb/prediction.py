from fantasystats.models.nba import prediction
from mongoengine import DoesNotExist


def save_prediction(
    game_key,
    game_date,
    away_team,
    home_team,
    winner,
    provider,
    game_url,
    payload
):

    pred_key = '%s-%s' % (
        game_key, provider
    )

    try:
        t = prediction.mlb_prediction.objects.get(prediction_key=pred_key)
        t.payload = payload
        t.winner = winner
        t.save()
    except DoesNotExist:
        t = prediction.mlb_prediction(
            game_key=game_key,
            game_date=game_date,
            away_team=away_team,
            home_team=home_team,
            winner=winner,
            provider=provider,
            game_url=game_url,
            payload=payload,
            prediction_key=pred_key
        )
        t.save()

    return t


def get_prediction_by_game_key(game_key):
    return prediction.mlb_prediction.objects.filter(game_key=game_key)
