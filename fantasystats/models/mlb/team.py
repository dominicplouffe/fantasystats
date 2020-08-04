from mongoengine import Document, StringField


class mlb_team(Document):
    full_name = StringField(required=True)
    short_name = StringField(required=True)
    team_code = StringField(required=True)
    abbr = StringField(required=True)
    name = StringField(required=True)
    location_name = StringField(required=True)
    league = StringField(required=True)
    division = StringField(required=True)
    venue = StringField(required=True)
    name_search = StringField(required=True)
    color1 = StringField(required=False)
    color2 = StringField(required=False)
    color3 = StringField(required=False)


def create_indexes():
    mlb_team.create_index([('team_code', 1)])
    mlb_team.create_index([('abbr', 1)])
    mlb_team.create_index([('name_search', 1)])
