from fantasystats.models.mlb import game
from mongoengine import DoesNotExist, Q
from fantasystats.services import search
from datetime import datetime


def insert_game(
    mlb_id,
    venue,
    game_date,
    game_time,
    game_ampm,
    start_time,
    double_header,
    game_type,
    home_team,
    away_team,
    home_pitcher,
    away_pitcher,
    game_number,
    season,
    game_status,
    winner_side=None,
    winner_name=None,
    team_scoring=0,
    innings=0,
    current_inning=0,
    is_top=False,
    update=False
):

    game_key = search.create_game_key(
        game_date, away_team, home_team, double_header, game_number
    )

    try:
        g = game.mlb_game.objects.get(game_key=game_key)

        if update:
            g.game_key = game_key
            g.mlb_id = mlb_id
            g.venue = search.get_search_value(venue)
            g.game_date = game_date
            g.game_time = game_time
            g.game_ampm = game_ampm
            g.start_time = start_time
            g.double_header = double_header
            g.game_type = game_type
            g.home_team = search.get_search_value(home_team)
            g.away_team = search.get_search_value(away_team)
            g.home_pitcher = search.get_search_value(home_pitcher)
            g.away_pitcher = search.get_search_value(away_pitcher)
            g.game_number = game_number
            g.season = season
            g.game_status = game_status
            g.winner_side = winner_side
            g.winner_name = winner_name
            g.team_scoring = team_scoring
            g.innings = innings
            g.current_inning = current_inning
            g.is_top = is_top
            g.save()
    except DoesNotExist:

        g = game.mlb_game(
            game_key=game_key,
            mlb_id=mlb_id,
            venue=search.get_search_value(venue),
            game_date=game_date,
            game_time=game_time,
            game_ampm=game_ampm,
            start_time=start_time,
            double_header=double_header,
            game_type=game_type,
            home_team=search.get_search_value(home_team),
            away_team=search.get_search_value(away_team),
            home_pitcher=search.get_search_value(home_pitcher),
            away_pitcher=search.get_search_value(away_pitcher),
            game_number=game_number,
            season=season,
            game_status=game_status,
            winner_side=winner_side,
            winner_name=winner_name,
            team_scoring=team_scoring,
            innings=innings,
            current_inning=current_inning,
            is_top=is_top
        )
        g.save()

    return g


def get_game_by_key(game_key):

    try:
        g = game.mlb_game.objects.get(game_key=game_key)

        return g
    except DoesNotExist:
        return None


def get_by_game_date(game_date):

    start_date = datetime(game_date.year, game_date.month, game_date.day, 0, 0)
    end_date = datetime(game_date.year, game_date.month, game_date.day, 23, 59)
    return game.mlb_game.objects.filter(
        Q(game_date__gte=start_date) & Q(game_date__lte=end_date)
    ).order_by('game_date')


def get_games_by_season(season, team_name=None):

    if team_name:
        team_name = search.get_search_value(team_name)
        return game.mlb_game.objects.filter(
            Q(season=season) & (Q(home_team=team_name) | Q(away_team=team_name))
        )

    return game.mlb_game.objects.filter(
        season=season
    )


def get_team_names(season):

    return game.mlb_game.objects.filter(
        season=season
    ).distinct('home_team')


def get_game_by_mlb_id(mlb_id):
    try:
        g = game.mlb_game.objects.get(mlb_id=mlb_id)

        return g
    except DoesNotExist:
        return None
