from fantasystats.models.nba import gameplayer
from mongoengine import DoesNotExist, Q
from fantasystats.services import search


def insert_gameplayer(
    game_key,
    player_name,
    game_date,
    season,
    game_type,
    team_name,
    position,
    is_starter,
    dnp_reason,
    stats,
    update=False
):

    gameplayer_key = search.create_gameplayer_key(
        game_key,
        team_name,
        player_name
    )

    try:
        gp = gameplayer.nba_gameplayer.objects.get(
            gameplayer_key=gameplayer_key)

        if update:
            gp.game_key = game_key
            gp.player_name = search.get_search_value(player_name)
            gp.game_date = game_date
            gp.season = season
            gp.game_type = game_type
            gp.team_name = search.get_search_value(team_name)
            gp.position = position
            gp.is_starter = is_starter
            gp.dnp_reason = dnp_reason
            gp.stats = stats
            gp.gameplayer_key = gameplayer_key
            gp.save()

    except DoesNotExist:
        gp = gameplayer.nba_gameplayer(
            game_key=game_key,
            player_name=search.get_search_value(player_name),
            team_name=search.get_search_value(team_name),
            game_date=game_date,
            season=season,
            game_type=game_type,
            position=position,
            is_starter=is_starter,
            dnp_reason=dnp_reason,
            stats=stats,
            gameplayer_key=gameplayer_key
        )
        gp.save()

    return gp


def get_gameplayers_by_game_key(game_key):

    return gameplayer.nba_gameplayer.objects.filter(game_key=game_key)


def get_gameplayers_by_team(season, team_name, to_date=None):

    if to_date:
        return gameplayer.nba_gameplayer.objects.filter(
            Q(season=season) & Q(team_name=search.get_search_value(
                team_name)) & Q(game_date__lt=to_date) & Q(game_type='R') &
            (Q(game_type='R') or Q(game_type='FR'))
        )

    return gameplayer.nba_gameplayer.objects.filter(
        Q(season=season) & Q(team_name=search.get_search_value(team_name))
    )


def get_gameplayer_by_name(player_name):
    return gameplayer.nba_gameplayer.objects.filter(
        player_name=search.get_search_value(player_name)
    ).order_by('-game_date')


def get_gameplayer_by_date(game_date):
    return gameplayer.nba_gameplayer.objects.filter(
        game_date=game_date
    )


def get_distince_gameplayer_by_team(season, team_name):
    return gameplayer.nba_gameplayer.objects.filter(
        Q(season=season) & Q(team_name=team_name)
    ).distinct('player_name')
