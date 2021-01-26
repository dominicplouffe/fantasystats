from fantasystats.models.nba import team
from mongoengine import DoesNotExist
from fantasystats.services import search


def insert_team(
    full_name,
    short_name,
    team_code,
    abbr,
    name,
    location_name,
    conference,
    division,
    venue=None,
    color1=None,
    color2=None,
    color3=None
):

    name_search = search.get_search_value(full_name)

    try:
        t = team.nba_team.objects.get(name_search=name_search)
    except DoesNotExist:
        t = team.nba_team(
            full_name=full_name,
            short_name=short_name,
            team_code=team_code,
            abbr=abbr,
            name=name,
            location_name=location_name,
            conference=conference,
            division=division,
            venue=search.get_search_value(venue) if venue else None,
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
        t = team.nba_team.objects.get(name_search=name_search)

        return t
    except DoesNotExist:
        return None


def get_team_by_shortname(short_name):
    try:
        t = team.nba_team.objects.get(short_name=short_name)

        return t
    except DoesNotExist:
        return None


def get_teams():

    return team.nba_team.objects.all()


def get_team_by_abbr(abbr):
    try:
        t = team.nba_team.objects.filter(abbr=abbr)

        return t
    except DoesNotExist:
        return None
