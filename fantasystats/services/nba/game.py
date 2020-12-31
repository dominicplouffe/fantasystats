from datetime import datetime
from fantasystats import context
from fantasystats.managers.nba import (
    game, team, venue, player, gameplayer, fantasy, season
)


def get_seasons():

    return [s.season_name for s in season.get_seasons()]


def get_all_teams(season):

    all_teams = game.get_team_names(season)
    all_teams = sorted(all_teams)

    teams = []

    for t in all_teams:
        t = get_team(t)
        teams.append(t)

    return teams


def get_team(team_name, standings=False, season=None, to_date=None):

    if standings and not season:
        raise ValueError(
            'season must be added as an argument is standings is passed')

    if season and not standings:
        raise ValueError(
            'standings must be added as an argument is season is passed')

    standings_res = None
    team_info = team.get_team_by_name(team_name)

    if standings:
        standings_res = get_standings(
            season, team_name=team_info.name_search, to_date=to_date)
        standings_res.pop('team')

    return {
        'full_name': team_info.full_name,
        'name': team_info.name,
        'location_name': team_info.location_name,
        'conference': team_info.conference,
        'division': team_info.division,
        'abbr': team_info.abbr,
        'team_id': team_info.name_search,
        'color1': team_info.color1,
        'color2': team_info.color2,
        'color3': team_info.color3,
        'logo': 'https://fantasydataobj.s3.us-east-2.amazonaws.com'
                '/mba/teams/%s.png' % (
                    team_info.name_search
                ),
        'standings': standings_res
    }


def get_player(player_name):

    player_info = {
        'bio': get_player_bio(player_name),
        'seasons': {},
        'stats': _init_player_stats()
    }

    all_games = gameplayer.get_gameplayer_by_name(player_name)

    for g in all_games:
        if g.season not in player_info['seasons']:
            player_info['seasons'][g.season] = _init_player_stats()

        player_info['seasons'][g.season] = _increment_stats(
            player_info['seasons'][g.season],
            g
        )

        player_info['stats'] = _increment_stats(
            player_info['stats'],
            g
        )

    return player_info


def get_player_bio(player_name):

    player_info = player.get_player_by_name(player_name)

    if not player_info:
        return {}

    return {
        'name': player_info.full_name,
        'primary_number': player_info.primary_number,
        'position': player_info.position,
        'birth_date': player_info.birth_date,
        'birth_country': player_info.birth_country,
        'player_id': player_info.name_search,
        'draft_year': player_info.draft_year,
        'affiliation': player_info.affiliation,
        'school_type': player_info.schoolType,
        'weight': player_info.weight,
        'height': player_info.height,
        'headshot': 'https://fantasydataobj.s3.us-east-2.amazonaws.com'
                    '/nba/players/%s' % player_info.player_img
    }


def get_team_details(season, team_name, to_date=None):

    team_info = get_team(team_name)
    standings = get_standings(season, team_name=team_name, to_date=to_date)

    gameplayers = gameplayer.get_gameplayers_by_team(
        season,
        team_name,
        to_date=to_date
    )

    all_players = {}
    stats = _init_player_stats()
    for p in gameplayers:
        if p.game_type != '2':
            continue
        if p.player_name not in all_players:
            all_players[p.player_name] = {
                'bio': get_player_bio(p.player_name),
                'stats': _init_player_stats()
            }

        all_players[p.player_name]['stats'] = _increment_stats(
            all_players[p.player_name]['stats'],
            p
        )

        stats = _increment_stats(
            stats, p
        )

    num_games = standings['games']
    if num_games == 0:
        num_games = 1

    stats['points_per_game'] = stats['points'] / num_games
    stats['assists_per_game'] = stats['assists'] / num_games
    stats['blocks_per_game'] = stats['blocks'] / num_games
    stats['steals_per_game'] = stats['steals'] / num_games
    stats['rebs_per_game'] = stats['rebs'] / num_games
    stats['def_rebs_per_game'] = stats['def_rebs'] / num_games
    stats['fgm_per_game'] = stats['fgm'] / num_games
    stats['tpm_per_game'] = stats['tpm'] / num_games
    stats['ftm_per_game'] = stats['ftm'] / num_games
    stats['fouls_per_game'] = stats['fouls'] / num_games

    return {
        'details': team_info,
        'standings': standings,
        'players': all_players,
        'team_stats': stats
    }


def get_standings(season, team_name=None, by='nba', to_date=None):

    if by not in ['conference', 'nba', 'division']:
        raise ValueError

    all_games = game.get_games_by_season(season, team_name=team_name)

    games = {}

    for g in all_games:

        if g.game_type != '2':
            continue
        home = get_team(g.home_team)
        away = get_team(g.away_team)

        if home['division'] == 'n/a':
            continue
        if g.home_team not in games:
            games[g.home_team] = {
                'team': home,
                'games': 0,
                'wins': 0,
                'losses': 0,
                'win_per': 0.00,
                'points_for': 0,
                'points_against': 0,
                'points_diff': 0,
                'home': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'win_per': 0.00
                },
                'away': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'win_per': 0.00
                },
            }
        if g.away_team not in games:
            games[g.away_team] = {
                'team': away,
                'games': 0,
                'wins': 0,
                'losses': 0,
                'win_per': 0.00,
                'points_for': 0,
                'points_against': 0,
                'points_diff': 0,
                'home': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'win_per': 0.00
                },
                'away': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'win_per': 0.00
                },
            }
        if to_date and to_date <= g.game_date:
            break
        if g.game_status not in ['Final', 'Preview']:
            continue

        games[g.home_team]['games'] += 1
        games[g.home_team]['home']['games'] += 1
        games[g.away_team]['games'] += 1
        games[g.away_team]['away']['games'] += 1

        games[g.home_team]['points_for'] += g.team_scoring['home']['score']
        games[g.home_team]['points_against'] += g.team_scoring['away']['score']

        games[g.away_team]['points_for'] += g.team_scoring['away']['score']
        games[g.away_team]['points_against'] += g.team_scoring['home']['score']

        games[g.home_team]['points_diff'] = games[g.home_team][
            'points_for'] - games[g.home_team]['points_against']
        games[g.away_team]['points_diff'] = games[g.away_team][
            'points_for'] - games[g.away_team]['points_against']

        if g.winner_side == 'home':
            games[g.home_team]['wins'] += 1
            games[g.home_team]['home']['wins'] += 1

            games[g.away_team]['losses'] += 1
            games[g.away_team]['away']['losses'] += 1

        else:
            games[g.away_team]['wins'] += 1
            games[g.away_team]['away']['wins'] += 1

            games[g.home_team]['losses'] += 1
            games[g.home_team]['home']['losses'] += 1

        games[g.home_team]['win_per'] = (
            games[g.home_team]['wins'] / games[g.home_team]['games']
        )
        games[g.away_team]['win_per'] = (
            games[g.away_team]['wins'] / games[g.away_team]['games']
        )

        if games[g.home_team]['home']['games'] > 0:
            games[g.home_team]['home']['win_per'] = (
                games[g.home_team]['home']['wins'] /
                games[g.home_team]['home']['games']
            )
        if games[g.home_team]['away']['games'] > 0:
            games[g.home_team]['away']['win_per'] = (
                games[g.home_team]['away']['wins'] /
                games[g.home_team]['away']['games']
            )

        if games[g.away_team]['home']['games'] > 0:
            games[g.away_team]['home']['win_per'] = (
                games[g.away_team]['home']['wins'] /
                games[g.away_team]['home']['games']
            )
        if games[g.away_team]['away']['games'] > 0:
            games[g.away_team]['away']['win_per'] = (
                games[g.away_team]['away']['wins'] /
                games[g.away_team]['away']['games']
            )

    games = games.values()
    games = sorted(games, key=lambda x: -x['win_per'])

    if team_name:
        for g in games:
            if g['team']['team_id'] == team_name:
                return g
    if by == 'nba':
        return games
    elif by == 'league':
        leagues = {}
        for g in games:
            if g['team']['league'] not in leagues:
                leagues[g['team']['league']] = []
            leagues[g['team']['league']].append(g)

        return leagues
    elif by == 'division':
        divisions = {}
        for g in games:
            if g['team']['division'] not in divisions:
                divisions[g['team']['division']] = []
            divisions[g['team']['division']].append(g)

        return divisions


def get_games_by_date(game_date):

    now_date = datetime.utcnow()
    now_date = datetime(now_date.year, now_date.month, now_date.day)

    if game_date >= now_date:
        all_games = game.get_by_game_date(game_date)
    else:
        all_games = [
            g for g in game.get_by_game_date(game_date)
            if g.game_status != "Preview"
        ]

    return [
        get_game_by_key(
            g.game_key,
            game_info=g,
            include_players=False,
            to_date=game_date,
            include_odds=True
        )
        for g in all_games
    ]


def get_game_by_key(
    game_key,
    game_info=None,
    include_players=True,
    include_odds=False,
    to_date=None
):

    if not game_info:
        game_info = game.get_game_by_key(game_key)

    if game_info is None:
        return {}

    home_team_name = game_info.home_team
    away_team_name = game_info.away_team

    game_info.home_team = get_team(
        game_info.home_team,
        standings=True,
        season=game_info.season,
        to_date=to_date
    )
    game_info.away_team = get_team(
        game_info.away_team,
        standings=True,
        season=game_info.season,
        to_date=to_date
    )
    game_info.venue = get_venue(game_info.venue)
    game_info.id = None

    game_info = game_info.to_mongo()
    if include_players:
        game_info['players'] = get_game_players(
            game_key,
            home_team_name,
            away_team_name,
        )

    if include_odds:
        odds = context.db.nba_odds.find_one({
            '_id': game_key
        })

        if odds:
            odds.pop('_id')
            odds.pop('game_key')
            game_info['odds'] = odds

    return game_info


def get_venue(venue_name):

    venue_info = venue.get_venue_by_name(venue_name)

    if venue_info is None:
        return {
            'venue_name': 'n/a'
        }

    return {
        'venue_name': venue_info['name']
    }


def get_game_players(game_key, home_team, away_team):

    gameplayers = gameplayer.get_gameplayers_by_game_key(game_key)

    all_players = {
        'home': [],
        'away': [],
    }

    for p in gameplayers:

        player_info = get_player_bio(p.player_name)
        if not player_info:
            continue

        fantasy_info = fantasy.get_fantasy_by_gameplayer_key(
            p.gameplayer_key
        )
        fantasy_data = {'FanDuel': {'price': 0}}
        if fantasy_info:
            fantasy_data['FanDuel'] = {'price': fantasy_info.price}
        player_info['fantasy'] = fantasy_data

        ply = p.stats
        ply['bio'] = player_info
        ply['player_name'] = player_info['name']
        ply['player_id'] = p['player_name']
        if p.team_name == home_team:
            all_players['home'].append(ply)
        else:
            all_players['away'].append(ply)

    all_players['home'] = sorted(
        all_players['home'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )

    all_players['away'] = sorted(
        all_players['away'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )

    return all_players


def get_versus(season, away_team, home_team):

    return {
        'home': get_team_details(season, home_team),
        'away': get_team_details(season, away_team)
    }


def _increment_stats(stats, gameplayer_info):

    stats['games_played'] += 1
    for k, v in gameplayer_info['stats'].items():
        if v is None:
            continue
        stats[k] += v

    if stats['fga'] > 0:
        stats['fgpct'] = stats['fgm'] / stats['fga']

    if stats['fta'] > 0:
        stats['ftpct'] = stats['ftm'] / stats['fta']

    if stats['tpa'] > 0:
        stats['tppct'] = stats['tpm'] / stats['tpa']

    stats['points_per_game'] = stats['points'] / stats['games_played']
    stats['assists_per_game'] = stats['assists'] / stats['games_played']
    stats['blocks_per_game'] = stats['blocks'] / stats['games_played']
    stats['steals_per_game'] = stats['steals'] / stats['games_played']
    stats['rebs_per_game'] = stats['rebs'] / stats['games_played']
    stats['def_rebs_per_game'] = stats['def_rebs'] / stats['games_played']
    stats['fgm_per_game'] = stats['fgm'] / stats['games_played']
    stats['tpm_per_game'] = stats['tpm'] / stats['games_played']
    stats['ftm_per_game'] = stats['ftm'] / stats['games_played']
    stats['fouls_per_game'] = stats['fouls'] / stats['games_played']

    return stats


def _init_player_stats():

    stats = {
        'games_played': 0,
        'assists': 0,
        'blocks': 0,
        'def_rebs': 0,
        'fga': 0,
        'fgm': 0,
        'fgpct': 0,
        'fouls': 0,
        'fta': 0,
        'ftm': 0,
        'ftpct': 0,
        'mins': 0,
        'off_rebs': 0,
        'points': 0,
        'rebs': 0,
        'secs': 0,
        'steals': 0,
        'tpa': 0,
        'tpm': 0,
        'tppct': 0,
        'turnovers': 0,

        'points_per_game': 0,
        'assists_per_game': 0,
        'blocks_per_game': 0,
        'steals_per_game': 0,
        'rebs_per_game': 0,
        'def_rebs_per_game': 0,
        'fgm_per_game': 0,
        'tpm_per_game': 0,
        'ftm_per_game': 0,
        'fouls_per_game': 0
    }

    return stats