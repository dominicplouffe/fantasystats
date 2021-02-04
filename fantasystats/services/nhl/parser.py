import re
from datetime import datetime, timedelta
from fantasystats import context
from fantasystats.managers.nhl import (
    season, venue, team, player, game, gameplayer
)


def process_data(data, update=False):

    try:
        game_data = data['gameData']
        if 'broadcasters' in data:
            game_data['broadcasters'] = data['broadcasters']
        else:

            start_time = datetime.strptime(
                game_data['datetime']['dateTime'],
                '%Y-%m-%dT%H:%M:%SZ'
            )
            start_time = start_time - timedelta(hours=5)
            game_date = datetime(
                start_time.year, start_time.month, start_time.day
            )

            g = game.get_game_by_nhl_id(
                game_data['game']['pk'], game_date
            )
            if g:
                game_data['broadcasters'] = g.broadcasters

        game_season = game_data['game']['season']
        teams = game_data['teams']

        season.insert_season(game_season)

        process_venue(teams['home']['venue'])
        process_venue(teams['away']['venue'])

        venue.get_venue_by_name(
            game_data['venue']['name']
        )

        process_team(teams['home'])
        process_team(teams['away'])

        for key, game_player in game_data['players'].items():
            process_player(game_player)

        line_score = data['liveData']['linescore']
        game_info = process_game(
            game_data,
            line_score,
            update=update
        )

        for key, box_player in data[
                'liveData']['boxscore']['teams']['away']['players'].items():
            process_gameplayer(game_info, box_player, False, update=update)

        for key, box_player in data[
                'liveData']['boxscore']['teams']['home']['players'].items():
            process_gameplayer(game_info, box_player, True, update=update)

        context.logger.info(game_info.game_key)
    except KeyError as e:
        context.logger.info('Key Error: %s' % e)


def process_gameplayer(game_info, box_player, is_home, update=False):

    team_name = game_info.home_team if is_home else game_info.away_team
    game_key = game_info.game_key
    game_date = game_info.game_date
    season = game_info.season

    player_name = box_player['person']['fullName']
    position = box_player.get('position', {}).get('abbreviation', 'n/a')
    player_status = box_player['person']['rosterStatus']

    is_goalie = len(box_player['stats'].get('goalieStats', [])) > 0
    is_skater = len(box_player['stats'].get('skaterStats', [])) > 0

    stats = {
        'goalie': {},
        'skater': {}
    }

    if is_goalie:
        for k, v in box_player['stats']['goalieStats'].items():
            key, value = _convert_key_value_pair(k, v)
            stats['goalie'][key] = value

    if is_skater:
        for k, v in box_player['stats']['skaterStats'].items():
            key, value = _convert_key_value_pair(k, v)
            stats['skater'][key] = value

    gameplayer.insert_gameplayer(
        game_key,
        player_name,
        game_date,
        season,
        game_info.game_type,
        team_name,
        position,
        player_status,
        is_goalie,
        is_skater,
        stats,
        update=update
    )


def process_game(
    game_data, line_score, update=False
):

    start_time = datetime.strptime(
        game_data['datetime']['dateTime'],
        '%Y-%m-%dT%H:%M:%SZ'
    )
    start_time = start_time - timedelta(hours=5)
    game_date = datetime(start_time.year, start_time.month, start_time.day)

    home_goals = line_score['teams']['home'].get('goals', 0)
    away_goals = line_score['teams']['away'].get('goals', 0)

    if away_goals > home_goals:
        winner_side = 'away'
        winner_name = game_data['teams']['away']['name']
    else:
        winner_side = 'home'
        winner_name = game_data['teams']['home']['name']

    current_period = line_score.get('currentPeriod', 0)
    periods = []
    for i in line_score.get('periods', []):
        inn = {}
        for k, v in i.items():
            if k in ["ordinalNum", "startTime", "endTime"]:
                continue
            inn[k] = v
        periods.append(inn)

    team_scoring = {}
    for t, team_info in line_score.get('teams', {}).items():
        team_side = t
        scoring = {}
        for k, v in team_info.items():
            if k in ['team']:
                continue
            key, value = _convert_key_value_pair(k, v)
            scoring[key] = value
        team_scoring[team_side] = scoring

    broadcasters = game_data.get('broadcasters', [])
    attendance = 0

    status = game_data['status']['detailedState']

    game_info = game.insert_game(
        game_data['game']['pk'],
        game_data['venue']['name'],
        game_date,
        start_time,
        game_data['game']['type'],
        game_data['teams']['home']['name'],
        game_data['teams']['away']['name'],
        game_data['game']['season'],
        status,
        winner_side=winner_side,
        winner_name=winner_name,
        team_scoring=team_scoring,
        periods=periods,
        current_period=current_period,
        broadcasters=broadcasters,
        attendance=attendance,
        update=update
    )

    return game_info


def process_player(game_player):

    full_name = game_player['fullName']
    name = game_player['fullName']
    first_name = game_player['firstName']
    last_name = game_player['lastName']
    primary_number = game_player.get('primaryNumber', 'n/a')
    birth_city = game_player.get('birthCity', 'n/a')
    birth_state = game_player.get('birthStateProvince', 'n/a')
    birth_country = game_player.get('birthCountry', 'n/a')
    height = game_player.get('height', 'n/a')
    weight = game_player.get('weight', 0)
    position = game_player['primaryPosition']['abbreviation']
    shoot_catch_side = game_player.get('shootsCatches', 'n/a')
    nhl_id = game_player['id']

    if 'birthDate' in game_player:
        birth_date = datetime.strptime(game_player['birthDate'], '%Y-%m-%d')
    else:
        birth_date = None

    p = player.insert_player(
        full_name,
        name,
        first_name,
        last_name,
        primary_number,
        birth_date,
        birth_city,
        birth_state,
        birth_country,
        weight,
        height,
        position,
        shoot_catch_side,
        nhl_id
    )

    return p


def process_venue(game_venue):
    name = game_venue['name']
    city = game_venue['city']
    timezone = game_venue['timeZone']

    v = venue.insert_venue(
        name,
        city,
        timezone,
    )

    return v


def process_team(game_team, update=False):

    full_name = game_team['name']
    short_name = game_team['shortName']
    team_code = game_team['triCode']
    abbr = game_team['abbreviation']
    name = game_team['teamName']
    location_name = game_team.get('locationName', 'n/a')

    conference = game_team['conference']['name']
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
        conference,
        division,
        venue
    )

    return t


def _convert_key_value_pair(k, v):
    key = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()

    return key, v
