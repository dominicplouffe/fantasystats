from mongoengine import Document, StringField, FloatField, DictField


class mlb_venue(Document):
    name = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    state_abbr = StringField(required=True)
    latitude = FloatField()
    longitude = FloatField()
    timezone = DictField()
    field_info = DictField()
    name_search = StringField(required=True)


def create_indexes():
    mlb_venue.create_index([('name', 1)])
