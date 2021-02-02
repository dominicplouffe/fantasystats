from fantasystats.models.nhl import game
from mongoengine import DoesNotExist, Q, MultipleObjectsReturned
from fantasystats.services import search
from datetime import datetime


def insert_game(
    nhl_id,
    venue,
    game_date,
    start_time,
    game_type,
    home_team,
    away_team,
    season,
    game_status,
    winner_side=None,
    winner_name=None,
    team_scoring=0,
    periods=[],
    current_period=0,
    attendance=0,
    broadcasters=[],
    update=False
):

    game_key = search.create_game_key(
        game_date, away_team, home_team, 'N', '1'
    )

    try:
        g = game.nhl_game.objects.get(game_key=game_key)

        if update:
            g.game_key = game_key
            g.nhl_id = nhl_id
            g.venue = search.get_search_value(venue)
            g.game_date = game_date
            g.start_time = start_time
            g.game_type = game_type
            g.home_team = search.get_search_value(home_team)
            g.away_team = search.get_search_value(away_team)
            g.season = season
            g.game_status = game_status
            g.winner_side = winner_side
            g.winner_name = winner_name
            g.team_scoring = team_scoring
            g.periods = periods
            g.current_period = current_period
            g.attendance = attendance
            g.broadcasters = broadcasters
            g.save()
    except DoesNotExist:

        g = game.nhl_game(
            game_key=game_key,
            nhl_id=nhl_id,
            venue=search.get_search_value(venue),
            game_date=game_date,
            start_time=start_time,
            game_type=game_type,
            home_team=search.get_search_value(home_team),
            away_team=search.get_search_value(away_team),
            season=season,
            game_status=game_status,
            winner_side=winner_side,
            winner_name=winner_name,
            team_scoring=team_scoring,
            periods=periods,
            current_period=current_period,
            attendance=0,
            broadcasters=[],
        )
        g.save()

    return g


def get_game_by_key(game_key):

    try:
        g = game.nhl_game.objects.get(game_key=game_key)

        return g
    except DoesNotExist:
        return None


def get_by_game_date(game_date):

    start_date = datetime(game_date.year, game_date.month, game_date.day, 0, 0)
    end_date = datetime(game_date.year, game_date.month, game_date.day, 23, 59)
    return game.nhl_game.objects.filter(
        Q(game_date__gte=start_date) & Q(game_date__lte=end_date)
    ).order_by('game_date')


def get_games_by_season(season, team_name=None):

    if team_name:
        team_name = search.get_search_value(team_name)
        return game.nhl_game.objects.filter(
            Q(season=season) & (
                Q(home_team=team_name) | Q(away_team=team_name)
            )
        ).order_by('game_date')

    return game.nhl_game.objects.filter(
        season=season
    ).order_by('game_date')


def get_team_names(season):

    return game.nhl_game.objects.filter(
        season=season
    ).distinct('home_team')


def get_game_by_nhl_id(nhl_id, game_date):
    try:
        g = game.nhl_game.objects.get(nhl_id=nhl_id, game_date=game_date)

        return g
    except DoesNotExist:
        return None
    except MultipleObjectsReturned:

        print('*' * 100)
        print('Multiple Objects returned: %s' % nhl_id)
        return None
