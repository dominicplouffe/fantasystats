from fantasystats.models.mlb import season
from mongoengine import DoesNotExist


def insert_season(season_name):

    try:
        s = season.mlb_season.objects.get(season_name=season_name)
    except DoesNotExist:

        s = season.mlb_season(
            season_name=season_name
        )
        s.save()

    return s
