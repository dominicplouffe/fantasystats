from fantasystats.models.mlb import team
from mongoengine import DoesNotExist
from fantasystats.services import search


def insert_team(
    full_name,
    short_name,
    team_code,
    abbr,
    name,
    location_name,
    league,
    division,
    venue,
    color1=None,
    color2=None,
    color3=None
):

    name_search = search.get_search_value(full_name)

    try:
        t = team.mlb_team.objects.get(name_search=name_search)
    except DoesNotExist:
        t = team.mlb_team(
            full_name=full_name,
            short_name=short_name,
            team_code=team_code,
            abbr=abbr,
            name=name,
            location_name=location_name,
            league=league,
            division=division,
            venue=search.get_search_value(venue),
            name_search=name_search,
            color1=color1,
            color2=color2,
            color3=color3,
        )
        t.save()

    return t


def get_team_by_name(team_name):
    name_search = search.get_search_value(team_name)

    try:
        t = team.mlb_team.objects.get(name_search=name_search)

        return t
    except DoesNotExist:
        return None
