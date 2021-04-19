from fantasystats.models.nba import game
from mongoengine import DoesNotExist, Q
from fantasystats.services import search
from datetime import datetime


def insert_game(
    nba_id,
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
        g = game.nba_game.objects.get(game_key=game_key)

        if update:
            g.game_key = game_key
            g.nba_id = nba_id
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

        g = game.nba_game(
            game_key=game_key,
            nba_id=nba_id,
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
            broadcasters=broadcasters,
            attendance=attendance
        )
        g.save()

    return g


def get_game_by_key(game_key):

    try:
        g = game.nba_game.objects.get(game_key=game_key)

        return g
    except DoesNotExist:
        return None


def get_next_game(teama, teamb, game_date):

    games = game.nba_game.objects.filter(
        (Q(game_date__gte=game_date) & Q(
            home_team=search.get_search_value(teama)
        ) & Q(away_team=search.get_search_value(teamb))) | (
            Q(game_date__gte=game_date) & Q(
                home_team=search.get_search_value(teamb)
            ) & Q(away_team=search.get_search_value(teama))
        )
    ).order_by('game_date')

    if len(games) > 0:
        return games[0]

    return None


def get_by_game_date(game_date):

    start_date = datetime(game_date.year, game_date.month, game_date.day, 0, 0)
    end_date = datetime(game_date.year, game_date.month, game_date.day, 23, 59)
    return game.nba_game.objects.filter(
        Q(game_date__gte=start_date) & Q(game_date__lte=end_date)
    ).order_by('game_date')


def get_games_by_season(season, team_name=None):

    if team_name:
        team_name = search.get_search_value(team_name)
        return game.nba_game.objects.filter(
            Q(season=season) & (
                Q(home_team=team_name) | Q(away_team=team_name)
            )
        ).order_by('game_date')

    return game.nba_game.objects.filter(
        season=season
    ).order_by('game_date')


def get_team_names(season):

    return game.nba_game.objects.filter(
        season=season
    ).distinct('home_team')


def get_game_by_nba_id(nba_id):
    try:
        g = game.nba_game.objects.get(nba_id=nba_id)

        return g
    except DoesNotExist:
        return None
