from fantasystats.models.mlb import gameplayer
from mongoengine import DoesNotExist, Q
from fantasystats.services import search


def insert_gameplayer(
    game_key,
    player_name,
    game_date,
    season,
    game_number,
    game_type,
    team_name,
    position,
    player_status,
    is_batter,
    is_pitcher,
    is_fielder,
    stats,
    update=False
):

    gameplayer_key = search.create_gameplayer_key(
        game_key,
        team_name,
        player_name
    )

    try:
        gp = gameplayer.mlb_gameplayer.objects.get(
            gameplayer_key=gameplayer_key)

        if update:
            gp.game_key = game_key
            gp.player_name = search.get_search_value(player_name)
            gp.game_date = game_date
            gp.season = season
            gp.game_number = game_number
            gp.game_type = game_type
            gp.team_name = search.get_search_value(team_name)
            gp.position = position
            gp.player_status = player_status
            gp.is_batter = is_batter
            gp.is_pitcher = is_pitcher
            gp.is_fielder = is_fielder
            gp.stats = stats
            gp.gameplayer_key = gameplayer_key
            gp.save()

    except DoesNotExist:
        gp = gameplayer.mlb_gameplayer(
            game_key=game_key,
            player_name=search.get_search_value(player_name),
            team_name=search.get_search_value(team_name),
            game_date=game_date,
            season=season,
            game_number=game_number,
            game_type=game_type,
            position=position,
            player_status=player_status,
            is_batter=is_batter,
            is_pitcher=is_pitcher,
            is_fielder=is_fielder,
            stats=stats,
            gameplayer_key=gameplayer_key
        )
        gp.save()

    return gp


def get_gameplayers_by_game_key(game_key):

    return gameplayer.mlb_gameplayer.objects.filter(game_key=game_key)


def get_gameplayers_by_team(season, team_name, to_date=None):

    if to_date:
        return gameplayer.mlb_gameplayer.objects.filter(
            Q(season=season) & Q(team_name=search.get_search_value(
                team_name)) & Q(game_date__lte=to_date)
        )

    return gameplayer.mlb_gameplayer.objects.filter(
        Q(season=season) & Q(team_name=search.get_search_value(team_name))
    )


def get_gameplayer_by_name(player_name):
    return gameplayer.mlb_gameplayer.objects.filter(
        player_name=search.get_search_value(player_name)
    )


def get_gameplayer_by_date(game_date):
    return gameplayer.mlb_gameplayer.objects.filter(
        game_date=game_date
    )
