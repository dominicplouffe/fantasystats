from mongoengine import Document, StringField


class nhl_season(Document):
    season_name = StringField(required=True)


def create_indexes():
    nhl_season.create_index([('season_name', 1)])
