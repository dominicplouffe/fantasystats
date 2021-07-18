from mongoengine import Document, StringField, ListField, DateTimeField
from mongoengine import DictField


class match(Document):
    game_key = StringField(required=True)
    game_date = DateTimeField(required=True)
    start_time = DateTimeField(required=True)
    match_name = StringField(required=True)
    match_id = StringField(required=True)
    event_name = StringField(required=True)
    event_id = StringField(required=True)
    category = StringField(required=True)
    competitors = DictField(required=True)
    score = StringField(required=True)
    bets = ListField(required=True)


def create_indexes():
    match.create_index([('game_date', 1)])
    match.create_index([('game_key', 1)])
    match.create_index([('category', 1)])
    match.create_index([('match_name', 1)])
    match.create_index([('event_name', 1)])
