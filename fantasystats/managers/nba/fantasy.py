from fantasystats.models.nba import fantasy
from mongoengine import DoesNotExist
from fantasystats.services import search


def insert_fantasy(
    gameplayer_key,
    price,
    player_name,
    game_date,
    game_key,
    sportsbook
):

    player_name = search.get_search_value(player_name)

    try:
        t = fantasy.nba_fantasy.objects.get(gameplayer_key=gameplayer_key)
        t.gameplayer_key = gameplayer_key
        t.price = price
        t.player_name = player_name
        t.game_date = game_date
        t.game_key = game_key
        t.sportsbook = sportsbook
        t.save()
    except DoesNotExist:
        t = fantasy.nba_fantasy(
            gameplayer_key=gameplayer_key,
            price=price,
            player_name=player_name,
            game_date=game_date,
            game_key=game_key,
            sportsbook=sportsbook
        )
        t.save()

    return t


def get_fantasy_by_gameplayer_key(gameplayer_key):

    try:
        t = fantasy.nba_fantasy.objects.get(gameplayer_key=gameplayer_key)
        return t
    except DoesNotExist:
        return None


def get_fantansy_by_player_name(player_name):
    player_name = search.get_search_value(player_name)

    return fantasy.nba_fantasy.objects.filter(
        player_name=player_name
    ).order_by('-game_date')
