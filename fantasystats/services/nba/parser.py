import re
from datetime import datetime, timedelta
from fantasystats.managers.nba import (
    season, team, venue, player, game, gameplayer
)


def process_data(data, update=False):

    game_data = data['payload']

    game_season = season.get_season_from_game_date(
        datetime.strptime(
            game_data['gameProfile']['dateTimeEt'],
            '%Y-%m-%dT%H:%M'
        )
    )

    season.insert_season(game_season)

    process_team(game_data['homeTeam'])
    process_team(game_data['awayTeam'])

    venue = process_venue(game_data['gameProfile'])

    game_info = process_game(game_data, venue.name)

    for ply in game_data['homeTeam']['gamePlayers']:
        profile = ply['profile']
        process_player(profile)
        process_gameplayer(game_info, ply, True, update=update)

    for ply in game_data['awayTeam']['gamePlayers']:
        profile = ply['profile']
        process_player(profile)
        process_gameplayer(game_info, ply, False, update=update)


def process_team(game_team, update=False):

    full_name = '%s %s' % (
        game_team['profile']['cityEn'],
        game_team['profile']['nameEn']
    )
    short_name = game_team['profile']['nameEn']
    team_code = game_team['profile']['code']
    abbr = game_team['profile']['abbr']
    name = game_team['profile']['nameEn']
    location_name = game_team['profile'].get('cityEn', 'n/a')

    conference = game_team['profile']['conference']
    if 'division' in game_team['profile']:
        division = game_team['profile']['division']
    else:
        division = 'n/a'

    t = team.insert_team(
        full_name,
        short_name,
        team_code,
        abbr,
        name,
        location_name,
        conference,
        division
    )

    return t


def process_venue(game_venue):
    name = game_venue['arenaName']
    location = game_venue['arenaLocation']

    if name is None:
        name = 'Arena in %s' % location

    v = venue.insert_venue(
        name,
        location
    )

    return v


def process_player(game_player):
    full_name = game_player['displayNameEn']
    name = game_player['displayNameEn']
    first_name = game_player['firstNameEn']
    last_name = game_player['lastNameEn']
    name_code = game_player['code']
    primary_number = game_player['jerseyNo']
    birth_date = None
    birth_country = game_player['countryEn']
    weight = game_player['weight']
    if weight is None:
        weight = 0
    else:
        weight = int(weight.replace(' lbs', ''))
    height = game_player['height']
    position = game_player['position']
    draft_year = game_player['draftYear']
    if draft_year is None:
        draft_year = 0
    else:
        draft_year = int(draft_year)
    affiliation = game_player['displayAffiliation']
    schoolType = game_player['schoolType']
    nba_id = int(game_player['playerId'])

    if position is None:
        position = '?'

    if 'birthDate' in game_player:
        birth_date = datetime.fromtimestamp(
            int(game_player['dob']) / 1000
        )
    else:
        birth_date = None

    p = player.insert_player(
        full_name,
        name,
        first_name,
        last_name,
        name_code,
        primary_number,
        birth_date,
        birth_country,
        weight,
        height,
        position,
        draft_year,
        affiliation,
        schoolType,
        nba_id
    )

    return p


def process_game(game_data, venue, update=False):
    start_time = datetime.strptime(
        game_data['gameProfile']['dateTimeEt'],
        '%Y-%m-%dT%H:%M'
    )
    start_time = start_time - timedelta(hours=5)
    game_date = datetime(start_time.year, start_time.month, start_time.day)

    home_points = game_data['boxscore'].get('homeScore', 0)
    away_points = game_data['boxscore'].get('awayScore', 0)

    if away_points > home_points:
        winner_side = 'away'
        winner_name = game_data['awayTeam']['profile']['name']
    else:
        winner_side = 'home'
        winner_name = game_data['homeTeam']['profile']['name']

    periods = []
    for i in range(1, 5):
        per = {
            'period': i,
            'away_score': game_data['awayTeam'].get(
                'score', {}
            ).get('q%sScore' % i, 0),
            'home_score': game_data['homeTeam'].get(
                'score', {}
            ).get('q%sScore' % i, 0)
        }

        periods.append(per)

    team_scoring = {
        'home': {},
        'away': {}
    }

    for k, v in game_data['homeTeam'].get('score', {}).items():
        key, value = _convert_key_value_pair(k, v)
        team_scoring['home'][key] = value

    for k, v in game_data['awayTeam'].get('score', {}).items():
        key, value = _convert_key_value_pair(k, v)
        team_scoring['away'][key] = value

    game_status = game_data['boxscore']['statusDesc']
    current_period = game_data['boxscore']['period']

    if game_status is None:
        game_status = 'Not Started'

    game_info = game.insert_game(
        game_data['gameProfile']['gameId'],
        venue,
        game_date,
        start_time,
        game_data['gameProfile']['seasonType'],
        game_data['homeTeam']['profile']['name'],
        game_data['awayTeam']['profile']['name'],
        season.get_season_from_game_date(game_date),
        game_status,
        winner_side=winner_side,
        winner_name=winner_name,
        team_scoring=team_scoring,
        periods=periods,
        current_period=current_period,
        update=update
    )

    return game_info


def process_gameplayer(game_info, box_player, is_home, update=False):

    team_name = game_info.home_team if is_home else game_info.away_team
    game_key = game_info.game_key
    game_date = game_info.game_date
    season = game_info.season

    player_name = box_player['profile']['displayNameEn']
    position = box_player['boxscore']['position']
    is_starter = box_player['boxscore']['isStarter'] == "true"
    dnp_reason = box_player['boxscore']['dnpReason']

    stats = {}

    for k, v in box_player['statTotal'].items():
        key, value = _convert_key_value_pair(k, v)
        stats[key] = value

    gameplayer.insert_gameplayer(
        game_key,
        player_name,
        game_date,
        season,
        game_info.game_type,
        team_name,
        position,
        is_starter,
        dnp_reason,
        stats,
        update=update
    )


def _convert_key_value_pair(k, v):
    key = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()

    return key, v
