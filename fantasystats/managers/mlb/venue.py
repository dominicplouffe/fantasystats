from fantasystats.models.mlb import venue
from mongoengine import DoesNotExist
from fantasystats.services import search


def insert_venue(
    name,
    city,
    state,
    state_abbr,
    latitude,
    longitude,
    timezone,
    field_info,
):

    name_search = search.get_search_value(name)

    try:
        t = venue.mlb_venue.objects.get(name_search=name_search)
    except DoesNotExist:
        t = venue.mlb_venue(
            name=name,
            city=city,
            state=state,
            state_abbr=state_abbr,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            field_info=field_info,
            name_search=name_search
        )
        t.save()

    return t


def get_venue_by_name(name):
    name_search = search.get_search_value(name)

    try:
        t = venue.mlb_venue.objects.get(name_search=name_search)
        return t
    except DoesNotExist:
        return None
