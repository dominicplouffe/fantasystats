from fantasystats.models.nba import season
from mongoengine import DoesNotExist
from datetime import datetime


def get_season_from_game_date(gd):
    if gd >= datetime(2017, 10, 1) and gd <= datetime(2018, 6, 30):
        return '2017-2018'
    if gd >= datetime(2018, 10, 1) and gd <= datetime(2019, 6, 30):
        return '2018-2019'
    if gd >= datetime(2019, 10, 1) and gd <= datetime(2020, 10, 31):
        return '2019-2020'
    if gd >= datetime(2020, 12, 1) and gd <= datetime(2021, 6, 30):
        return '2020-2021'

    raise ValueError('Invalid date -> Season does not exist')


def insert_season(season_name):

    try:
        s = season.nba_season.objects.get(season_name=season_name)
    except DoesNotExist:

        s = season.nba_season(
            season_name=season_name
        )
        s.save()

    return s


def get_seasons():

    return season.nba_season.objects.all()
