from mongoengine import Document, StringField


class nba_venue(Document):
    name = StringField(required=True)
    location = StringField(required=True)

    name_search = StringField(required=True)


def create_indexes():
    nba_venue.create_index([('name', 1)])
    nba_venue.create_index([('name_search', 1)])
