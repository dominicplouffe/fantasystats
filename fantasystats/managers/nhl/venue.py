from fantasystats.models.nhl import venue
from mongoengine import DoesNotExist
from fantasystats.services import search


def insert_venue(
    name,
    city,
    timezone,
):

    name_search = search.get_search_value(name)

    try:
        t = venue.nhl_venue.objects.get(name_search=name_search)
    except DoesNotExist:
        t = venue.nhl_venue(
            name=name,
            city=city,
            timezone=timezone,
            name_search=name_search
        )
        t.save()

    return t


def get_venue_by_name(name):
    name_search = search.get_search_value(name)

    try:
        t = venue.nhl_venue.objects.get(name_search=name_search)
        return t
    except DoesNotExist:
        return None
