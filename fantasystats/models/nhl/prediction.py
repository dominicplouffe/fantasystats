from mongoengine import Document, StringField, DateTimeField, DictField


class nhl_prediction(Document):
    game_key = StringField(required=True)
    prediction_key = StringField(required=True)
    game_date = DateTimeField(required=True)
    away_team = StringField(required=True)
    home_team = StringField(required=True)
    winner = StringField(required=True)
    provider = StringField(required=True)
    game_url = StringField(required=True)
    payload = DictField(required=True)


def create_indexes():
    nhl_prediction.create_index([('game_key', 1)])
    nhl_prediction.create_index([('game_date', 1)])
    nhl_prediction.create_index([('away_team', 1)])
    nhl_prediction.create_index([('home_team', 1)])
    nhl_prediction.create_index([('prediction_key', 1)])
