import re
from datetime import datetime
from fantasystats import context
from fantasystats.managers.mlb import (
    season, team, venue, player, game, gameplayer
)


def process_data(data, update=False):
    try:
        game_data = data['gameData']
        game_season = game_data['game']['season']
        teams = game_data['teams']

        season.insert_season(game_season)

        home_team = process_team(teams['home'])
        away_team = process_team(teams['away'])

        game_venue = process_venue(game_data['venue'])

        for key, game_player in game_data['players'].items():
            process_player(game_player)

        line_score = data['liveData']['linescore']
        game_info = process_game(
            game_data,
            line_score,
            away_team,
            home_team,
            game_venue,
            update=update
        )

        for key, box_player in data[
                'liveData']['boxscore']['teams']['away']['players'].items():
            process_gameplayer(game_info, box_player, False, update=update)

        for key, box_player in data[
                'liveData']['boxscore']['teams']['home']['players'].items():
            process_gameplayer(game_info, box_player, True, update=update)
    except KeyError as e:
        context.logger.info('Key Error: %s' % e)


def process_game(
        game_data, line_score, away_team, home_team, game_venue, update=False
):

    game_date = datetime.strptime(
        game_data['datetime']['originalDate'], '%Y-%m-%d'
    )
    game_time = game_data['datetime']['time']
    game_ampm = game_data['datetime']['ampm']
    start_time = datetime.strptime(
        game_data['datetime']['dateTime'],
        '%Y-%m-%dT%H:%M:%SZ'
    )

    home_pitcher = ""
    away_pitcher = ""
    if 'home' in game_data['probablePitchers']:
        t = game_data['probablePitchers']['home']['fullName'].split(',')
        if len(t) == 2:
            home_pitcher = '%s %s' % (t[1].strip(), t[0].strip())
        else:
            home_pitcher = game_data['probablePitchers']['home']['fullName']

    if 'away' in game_data['probablePitchers']:
        t = game_data['probablePitchers']['away']['fullName'].split(',')
        if len(t) == 2:
            away_pitcher = '%s %s' % (t[1].strip(), t[0].strip())
        else:
            away_pitcher = game_data['probablePitchers']['away']['fullName']

    winner_side = None
    winner_name = None
    home_runs = line_score['teams']['home'].get('runs', 0)
    away_runs = line_score['teams']['away'].get('runs', 0)

    if away_runs > home_runs:
        winner_side = 'away'
        winner_name = game_data['teams']['away']['name']
    else:
        winner_side = 'home'
        winner_name = game_data['teams']['home']['name']

    current_inning = line_score.get('currentInning', 0)
    is_top = line_score.get('isTopInning', False)

    innings = []
    for i in line_score.get('innings', []):
        inn = {}
        for k, v in i.items():
            if k == "ordinalNum":
                continue
            key, value = _convert_key_value_pair(k, v)
            inn[key] = value
        innings.append(inn)

    team_scoring = {}
    for t, team_info in line_score.get('teams', {}).items():
        team_side = t
        scoring = {}
        for k, v in team_info.items():
            key, value = _convert_key_value_pair(k, v)
            scoring[key] = value
        team_scoring[team_side] = scoring

    game_info = game.insert_game(
        game_data['game']['pk'],
        game_data['venue']['name'],
        game_date,
        game_time,
        game_ampm,
        start_time,
        game_data['game']['doubleHeader'],
        game_data['game']['type'],
        game_data['teams']['home']['name'],
        game_data['teams']['away']['name'],
        home_pitcher,
        away_pitcher,
        game_data['game']['gameNumber'],
        game_data['game']['season'],
        game_data['status']['statusCode'],
        winner_side=winner_side,
        winner_name=winner_name,
        team_scoring=team_scoring,
        innings=innings,
        current_inning=current_inning,
        is_top=is_top,
        update=update
    )

    return game_info


def process_gameplayer(game_info, box_player, is_home, update=False):

    team_name = game_info.home_team if is_home else game_info.away_team
    game_key = game_info.game_key
    game_date = game_info.game_date
    season = game_info.season
    game_number = game_info.game_number

    player_name = box_player['person']['fullName']
    position = box_player.get('position', {}).get('abbreviation', 'n/a')
    player_status = box_player['status']['code']

    is_batter = len(box_player['stats']['batting']) > 0
    is_pitcher = len(box_player['stats']['pitching']) > 0
    is_fielder = len(box_player['stats']['fielding']) > 0

    stats = {
        'batting': {},
        'pitching': {},
        'fielding': {}
    }
    for k, v in box_player['stats']['batting'].items():
        if k == 'note':
            continue
        key, value = _convert_key_value_pair(k, v)
        stats['batting'][key] = value

    for k, v in box_player['stats']['pitching'].items():
        if k == 'note':
            continue
        key, value = _convert_key_value_pair(k, v)
        stats['pitching'][key] = value

    for k, v in box_player['stats']['fielding'].items():
        if k == 'note':
            continue
        key, value = _convert_key_value_pair(k, v)
        stats['fielding'][key] = value

    gameplayer.insert_gameplayer(
        game_key,
        player_name,
        game_date,
        season,
        game_number,
        game_info.game_type,
        team_name,
        position,
        player_status,
        is_batter,
        is_pitcher,
        is_fielder,
        stats,
        update=update
    )


def process_player(game_player):

    full_name = game_player['fullFMLName']
    name = game_player['lastFirstName']
    first_name = game_player['firstName']
    last_name = game_player['lastName']
    primary_number = game_player.get('primaryNumber', 'n/a')
    birth_city = game_player.get('birthCity', 'n/a')
    birth_state = game_player.get('birthStateProvince', 'n/a')
    birth_country = game_player.get('birthCountry', 'n/a')
    height = game_player['height']
    weight = game_player['weight']
    position = game_player['primaryPosition']['type']
    middle_name = game_player.get('middleName', 'n/a')
    box_score_name = game_player['firstLastName']
    bat_side = game_player['batSide']['code']
    pitch_side = game_player['pitchHand']['code']
    draft_year = game_player.get('draftYear', 0)
    mlb_id = game_player['id']

    if 'birthDate' in game_player:
        birth_date = datetime.strptime(game_player['birthDate'], '%Y-%m-%d')
    else:
        birth_date = None

    p = player.insert_player(
        full_name,
        name,
        first_name,
        last_name,
        middle_name,
        box_score_name,
        primary_number,
        birth_date,
        birth_city,
        birth_state,
        birth_country,
        weight,
        height,
        position,
        bat_side,
        pitch_side,
        draft_year,
        mlb_id
    )

    return p


def process_venue(game_venue):
    name = game_venue['name']
    city = game_venue['location']['city']
    state = game_venue['location'].get('state', 'n/a')
    state_abbr = game_venue['location'].get('stateAbbrev', 'n/a')

    latitude = None
    longitude = None
    if 'defaultCoordinates' in game_venue['location']:
        latitude = game_venue['location']['defaultCoordinates']['latitude']
        longitude = game_venue['location']['defaultCoordinates']['longitude']
    timezone = game_venue['timeZone']
    field_info = game_venue['fieldInfo']

    v = venue.insert_venue(
        name,
        city,
        state,
        state_abbr,
        latitude,
        longitude,
        timezone,
        field_info,
    )

    return v


def process_team(game_team, update=False):

    full_name = game_team['name']
    short_name = game_team['shortName']
    team_code = game_team['teamCode']
    abbr = game_team['abbreviation']
    name = game_team['teamName']
    location_name = game_team.get('locationName', 'n/a')
    league = game_team['league']['name']
    if 'division' in game_team:
        division = game_team['division']['name']
    else:
        division = 'n/a'
    venue = game_team['venue']['name']

    t = team.insert_team(
        full_name,
        short_name,
        team_code,
        abbr,
        name,
        location_name,
        league,
        division,
        venue
    )

    return t


def _convert_key_value_pair(k, v):
    key = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()

    if isinstance(v, str):
        if '--' in v:
            value = 0.00
        else:
            value = float(v)
    else:
        value = v

    return key, value
