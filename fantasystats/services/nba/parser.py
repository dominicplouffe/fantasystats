from fantasystats.managers.nba import (
    season, team
)

def process_data(data, update=False):

    game_data = data['payload']
    game_season = game_data['season']

    home_team = process_team(game_data['homeTeam'])
    away_team = process_team(game_data['awayTeam'])

    season.insert_season(game_season['yearDisplay'])

def process_team(game_team, update=False):

    print(game_team.keys())
    print('')
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