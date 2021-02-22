from mongoengine import (
    Document, StringField, IntField, DateTimeField, BooleanField,
    ListField, DictField
)


class mlb_game(Document):
    game_key = StringField(required=True)
    mlb_id = IntField(required=True)
    venue = StringField(required=True)
    game_date = DateTimeField(required=True)
    game_time = StringField(required=True)
    game_ampm = StringField(required=True)
    start_time = DateTimeField(required=True)
    double_header = StringField(required=True)
    game_type = StringField(required=True)
    home_team = StringField(required=True)
    away_team = StringField(required=True)
    home_pitcher = StringField(required=True)
    away_pitcher = StringField(required=True)
    game_number = IntField(required=True)
    season = StringField(required=True)
    game_status = StringField(required=True)
    winner_side = StringField(required=False)
    winner_name = StringField(required=False)
    team_scoring = DictField(request=False)
    innings = ListField(required=False)
    current_inning = IntField(required=True)
    is_top = BooleanField(required=True)
    broadcasters = ListField(required=False)


def create_indexes():
    mlb_game.create_index([('game_key', 1)])
    mlb_game.create_index([('mlb_id', 1)])
    mlb_game.create_index([('home_team', 1)])
    mlb_game.create_index([('away_pitcher', 1)])
    mlb_game.create_index([('season', 1)])
