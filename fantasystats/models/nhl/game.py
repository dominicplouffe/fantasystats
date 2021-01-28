from mongoengine import (
    Document, StringField, IntField, DateTimeField,
    ListField, DictField
)


class nhl_game(Document):
    game_key = StringField(required=True)
    nhl_id = IntField(required=True)
    venue = StringField(required=True)
    game_date = DateTimeField(required=True)
    start_time = DateTimeField(required=True)
    game_type = StringField(required=True)
    home_team = StringField(required=True)
    away_team = StringField(required=True)
    season = StringField(required=True)
    game_status = StringField(required=True)
    winner_side = StringField(required=False)
    winner_name = StringField(required=False)
    team_scoring = DictField(request=False)
    periods = ListField(required=False)
    current_period = IntField(required=True)
    attendance = IntField(required=False)
    broadcasters = ListField(required=False)


def create_indexes():
    nhl_game.create_index([('game_key', 1)])
    nhl_game.create_index([('nhl_id', 1)])
    nhl_game.create_index([('home_team', 1)])
    nhl_game.create_index([('away_team', 1)])
    nhl_game.create_index([('season', 1)])
