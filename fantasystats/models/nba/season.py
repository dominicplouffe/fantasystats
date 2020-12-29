from mongoengine import Document, StringField


class nba_season(Document):
    season_name = StringField(required=True)


def create_indexes():
    nba_season.create_index([('season_name', 1)])
