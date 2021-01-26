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
    try:
        t = prediction.nba_prediction.objects.get(game_key=game_key)
        t.payload = payload
        t.winner = winner
        t.save()
    except DoesNotExist:
        t = prediction.nba_prediction(
            game_key=game_key,
            game_date=game_date,
            away_team=away_team,
            home_team=home_team,
            winner=winner,
            provider=provider,
            game_url=game_url,
            payload=payload,
        )
        t.save()

    return t


def get_prediction_by_game_key(game_key):
    try:
        t = prediction.nba_prediction.objects.get(game_key=game_key)

        return t
    except DoesNotExist:
        return None
