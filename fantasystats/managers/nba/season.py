from fantasystats.models.nba import season
from mongoengine import DoesNotExist


def insert_season(season_name):

    try:
        s = season.nba_season.objects.get(season_name=season_name)
    except DoesNotExist:

        s = season.nba_season(
            season_name=season_name
        )
        s.save()

    return s
