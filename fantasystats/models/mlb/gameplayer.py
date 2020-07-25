from mongoengine import (
    StringField, DictField, Document, DateTimeField, IntField,
    BooleanField
)


class mlb_gameplayer(Document):

    gameplayer_key = StringField(required=True)
    game_key = StringField(required=True)
    player_name = StringField(required=True)
    game_date = DateTimeField(required=True)
    game_type = StringField(required=True)
    season = StringField(required=True)
    game_number = IntField(required=True)
    team_name = StringField(required=True)
    position = StringField(required=True)
    player_status = StringField(required=True)
    is_batter = BooleanField(required=True)
    is_pitcher = BooleanField(required=True)
    is_fielder = BooleanField(required=True)
    stats = DictField(required=True)


def create_indexes():
    mlb_gameplayer.create_index([('game_key', 1)])
    mlb_gameplayer.create_index([('gameplayer_key', 1)])
    mlb_gameplayer.create_index([('player_name', 1)])
