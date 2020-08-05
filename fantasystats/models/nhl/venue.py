from mongoengine import Document, StringField, FloatField, DictField


class nhl_venue(Document):
    name = StringField(required=True)
    city = StringField(required=True)
    timezone = DictField()
    name_search = StringField(required=True)


def create_indexes():
    nhl_venue.create_index([('name', 1)])
    nhl_venue.create_index([('name_search', 1)])
