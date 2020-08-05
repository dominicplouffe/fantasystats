from mongoengine import StringField, Document, DateTimeField, IntField


class nhl_player(Document):
    full_name = StringField(required=True)
    name = StringField(required=True)
    name_search = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    primary_number = StringField(required=False)
    birth_date = DateTimeField(required=False)
    birth_city = StringField(required=False)
    birth_state = StringField(required=False)
    birth_country = StringField(required=False)
    weight = IntField(required=False)
    height = StringField(required=False)
    position = StringField(required=True)
    shoot_catch_side = StringField(required=False)
    nhl_id = IntField(required=True)
    player_img = StringField(required=False)
    player_img_on = DateTimeField(required=False)


def create_indexes():
    nhl_player.create_index([('nhl_id', 1)])
    nhl_player.create_index([('name_search', 1)])
