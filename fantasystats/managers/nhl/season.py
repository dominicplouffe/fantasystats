from fantasystats.models.nhl import season
from mongoengine import DoesNotExist


def insert_season(season_name):

    try:
        s = season.nhl_season.objects.get(season_name=season_name)
    except DoesNotExist:

        s = season.nhl_season(
            season_name=season_name
        )
        s.save()

    return s


def get_seasons():

    return season.nhl_season.objects.all()
