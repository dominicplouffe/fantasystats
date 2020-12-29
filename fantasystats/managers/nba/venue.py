from fantasystats.models.nba import venue
from mongoengine import DoesNotExist
from fantasystats.services import search


def insert_venue(
    name,
    location
):

    name_search = search.get_search_value(name)

    try:
        t = venue.nba_venue.objects.get(name_search=name_search)
    except DoesNotExist:
        t = venue.nba_venue(
            name=name,
            location=location,
            name_search=name_search
        )
        t.save()

    return t


def get_venue_by_name(name):
    name_search = search.get_search_value(name)

    try:
        t = venue.nba_venue.objects.get(name_search=name_search)
        return t
    except DoesNotExist:
        return None
