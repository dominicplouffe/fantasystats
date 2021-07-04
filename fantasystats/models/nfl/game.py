from mongoengine import (
    Document, StringField, IntField, DateTimeField,
    ListField, DictField
)


class nfl_game(Document):
    game_key = StringField(required=True)
    nfl_id = IntField(required=True)
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
    current_periods = IntField(required=True)
    attendance = IntField(required=False)
    broadcasters = ListField(required=False)


def create_indexes():
    nfl_game.create_index([('game_key', 1)])
    nfl_game.create_index([('nfl_id', 1)])
    nfl_game.create_index([('home_team', 1)])
    nfl_game.create_index([('away_team', 1)])
    nfl_game.create_index([('season', 1)])
