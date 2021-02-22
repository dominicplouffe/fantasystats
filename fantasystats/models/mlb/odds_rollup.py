from mongoengine import (
    StringField, DictField, DateTimeField, Document, ListField
)


class mlb_oddsrollup(Document):

    rollup_id = StringField(required=True)
    noline = DictField(required=True)
    spread = DictField(required=True)
    over_under = DictField(required=True)
    points = DictField(required=True)
    team_id = StringField(required=True)
    rollup_date = DateTimeField(required=True)
    trends = ListField(required=False)


def create_indexes():
    mlb_oddsrollup.create_index([('rollup_id', 1)])
    mlb_oddsrollup.create_index([('team_id', 1)])
    mlb_oddsrollup.create_index([('rollup_date', 1)])
