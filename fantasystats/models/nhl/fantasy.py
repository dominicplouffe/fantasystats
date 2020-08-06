from mongoengine import Document, StringField, FloatField, DateTimeField


class nhl_fantasy(Document):
    gameplayer_key = StringField(required=True)
    price = FloatField(required=True)
    player_name = StringField(required=True)
    game_date = DateTimeField(required=True)
    game_key = StringField(required=True)
    sportsbook = StringField(required=True)


def create_indexes():
    nhl_fantasy.create_index([('gameplayer_key', 1)])
    nhl_fantasy.create_index([('player_name', 1)])
    nhl_fantasy.create_index([('game_date', 1)])
    nhl_fantasy.create_index([('game_key', 1)])
