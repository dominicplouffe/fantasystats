from mongoengine import (
    StringField, DictField, Document, DateTimeField,
    BooleanField
)


class nba_gameplayer(Document):

    gameplayer_key = StringField(required=True)
    game_key = StringField(required=True)
    player_name = StringField(required=True)
    game_date = DateTimeField(required=True)
    game_type = StringField(required=True)
    season = StringField(required=True)
    team_name = StringField(required=True)
    position = StringField(required=False)
    is_starter = BooleanField(required=True)
    dnp_reason = StringField(required=False)
    stats = DictField(required=True)


def create_indexes():
    nba_gameplayer.create_index([('game_key', 1)])
    nba_gameplayer.create_index([('gameplayer_key', 1)])
    nba_gameplayer.create_index([('player_name', 1)])
    nba_gameplayer.create_index([('game_date', 1)])
    nba_gameplayer.create_index(
        [('game_date', 1), ('season', 1), ('team_name', 1)])
