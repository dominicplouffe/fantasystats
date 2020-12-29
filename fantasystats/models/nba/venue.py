from mongoengine import Document, StringField, FloatField, DictField


class nba_venue(Document):
    name = StringField(required=True)
    location = StringField(required=True)
    name_search = StringField(required=True)


def create_indexes():
    mlb_venue.create_index([('name', 1)])
    mlb_venue.create_index([('name_search', 1)])
