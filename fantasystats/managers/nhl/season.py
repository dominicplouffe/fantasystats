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

    seasons = [
        (
            int(s.season_name[0:4]),
            s.season_name
        )
        for s in season.nhl_season.objects.all()
    ]
    seasons = sorted(seasons, key=lambda x: x[0])

    return [str(s[1]) for s in seasons]
