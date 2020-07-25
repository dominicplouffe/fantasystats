from mongoengine import Document, StringField


class mlb_season(Document):
    season_name = StringField(required=True)


def create_indexes():
    mlb_season.create_index([('season_name', 1)])
