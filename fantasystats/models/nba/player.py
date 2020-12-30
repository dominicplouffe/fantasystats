from mongoengine import StringField, Document, DateTimeField, IntField


class nba_player(Document):
    full_name = StringField(required=True)
    name = StringField(required=True)
    name_search = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    name_code = StringField(required=True)
    primary_number = StringField(required=False)
    birth_date = DateTimeField(required=False)
    birth_country = StringField(required=False)
    weight = IntField(required=False)
    height = StringField(required=False)
    position = StringField(required=True)
    draft_year = IntField(required=False)
    affiliation = StringField(required=False)
    schoolType = StringField(required=False)
    nba_id = IntField(required=True)
    player_img = StringField(required=False)
    player_img_on = DateTimeField(required=False)


def create_indexes():
    nba_player.create_index([('nba_id', 1)])
    nba_player.create_index([('name_search', 1)])
