import pytz
from datetime import datetime, timedelta
from fantasystats import context
from fantasystats.services import consensus
from fantasystats.managers.nhl import (
    game, team, venue, player, gameplayer, fantasy, season, prediction
)


def get_seasons():

    return [s.season_name for s in season.get_seasons()]


def get_games_by_date(game_date):

    now_date = datetime.utcnow()
    now_date = datetime(now_date.year, now_date.month, now_date.day)

    if game_date >= now_date:
        all_games = game.get_by_game_date(game_date)
    else:
        all_games = [
            g for g in game.get_by_game_date(game_date)
        ]

    return [
        get_game_by_key(
            g.game_key,
            game_info=g,
            include_players=False,
            to_date=game_date,
            include_odds=True,
            include_predictions=True,
            include_injuries=True
        )
        for g in all_games

    ]


def get_game_by_key(
    game_key,
    game_info=None,
    include_players=True,
    include_odds=False,
    include_predictions=False,
    include_injuries=False,
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

    if include_injuries:
        home_injuries = gameplayer.get_injured_players(home_team_name)
        away_injuries = gameplayer.get_injured_players(away_team_name)

        game_info['injuries'] = {
            'home_team': [
                {'bio': get_player_bio(k), 'since': v}
                for k, v in home_injuries.items()
            ],
            'away_team': [
                {'bio': get_player_bio(k), 'since': v}
                for k, v in away_injuries.items()
            ],
        }

    if include_odds:
        odds = context.db.nhl_odds.find_one({
            '_id': game_key
        })

        if odds:
            odds.pop('_id')
            odds.pop('game_key')
            game_info['odds'] = {
                'sites': odds,
                'consensus': consensus.get_odds_consensus(odds)
            }

    if include_predictions:
        preds = prediction.get_prediction_by_game_key(game_key)

        con_data = consensus.get_prediction_consensus(
            preds,
            game_info.get('odds', {}).get('consensus', [])
        )

        pred_sites = []
        for p in preds:
            con_data['picks'].get(p.provider, {})['winner'] = p.winner
            pred_sites.append({
                'provider': p.provider,
                'game_url': p.game_url,
                'predictions': p.payload,
                'picks': con_data['picks'].get(p.provider, {})
            })

        game_info['predictions'] = {
            'sites': pred_sites,
            'consensus': con_data['predictions']
        }

    game_info['attendance'] = 0
    game_info['broadcasters'] = game_info.get('broadcasters', [])

    game_info['start_time'] += timedelta(hours=5)

    return game_info


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
        'venue': get_venue(team_info.venue),
        'abbr': team_info.abbr,
        'team_id': team_info.name_search,
        'color1': team_info.color1,
        'color2': team_info.color2,
        'color3': team_info.color3,
        'logo': 'https://fantasydataobj.s3.us-east-2.amazonaws.com'
                '/nhl/teams/%s.png' % (
            team_info.name_search
        ),
        'standings': standings_res
    }


def get_versus(season, away_team, home_team):

    return {
        'home': get_team_details(season, home_team),
        'away': get_team_details(season, away_team)
    }


def get_venue(venue_name):

    venue_info = venue.get_venue_by_name(venue_name)

    if venue_info is None:
        return {
            'venue_name': 'n/a',
            'venue_location': 'n/a'
        }

    return {
        'venue_name': venue_info['name'],
        'venue_location': venue_info['city']
    }


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
        'shoot_catch_side': player_info.shoot_catch_side,
        'player_id': player_info.name_search,
        'headshot': 'https://fantasydataobj.s3.us-east-2.amazonaws.com'
                    '/nhl/players/%s' % player_info.player_img
    }


def get_game_players(game_key, home_team, away_team):

    gameplayers = gameplayer.get_gameplayers_by_game_key(game_key)

    all_players = {
        'home': {
            'skaters': [],
            'goalies': []
        },
        'away': {
            'skaters': [],
            'goalies': []
        },
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

        if p.is_skater:
            skater = p.stats['skater']
            skater['bio'] = player_info
            skater['player_name'] = player_info['name']
            skater['player_id'] = p['player_name']
            if p.team_name == home_team:
                all_players['home']['skaters'].append(skater)
            else:
                all_players['away']['skaters'].append(skater)
        if p.is_goalie:
            goalie = p.stats['goalie']
            goalie['bio'] = player_info
            goalie['player_name'] = player_info['name']
            goalie['player_id'] = p['player_name']
            if p.team_name == home_team:
                all_players['home']['goalies'].append(goalie)
            else:
                all_players['away']['goalies'].append(goalie)

    all_players['home']['skaters'] = sorted(
        all_players['home']['skaters'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )
    all_players['home']['goalies'] = sorted(
        all_players['home']['goalies'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )
    all_players['away']['skaters'] = sorted(
        all_players['away']['skaters'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )
    all_players['away']['goalies'] = sorted(
        all_players['away']['goalies'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )

    return all_players


def get_standings(season, team_name=None, by='nhl', to_date=None):

    if by not in ['conference', 'nhl', 'division']:
        raise ValueError

    all_games = game.get_games_by_season(season, team_name=team_name)

    games = {}

    for g in all_games:

        if g.game_type != 'R':
            continue

        if season == '20192020' and g.game_date > datetime(2020, 3, 10):
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
                'otl': 0,
                'win_per': 0.00,
                'goals_for': 0,
                'goals_against': 0,
                'goals_diff': 0,
                'home': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'otl': 0,
                    'win_per': 0.00
                },
                'away': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'otl': 0,
                    'win_per': 0.00
                },
            }
        if g.away_team not in games:
            games[g.away_team] = {
                'team': away,
                'games': 0,
                'wins': 0,
                'losses': 0,
                'otl': 0,
                'win_per': 0.00,
                'goals_for': 0,
                'goals_against': 0,
                'goals_diff': 0,
                'home': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'otl': 0,
                    'win_per': 0.00
                },
                'away': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'otl': 0,
                    'win_per': 0.00
                },
            }
        if to_date and to_date <= g.game_date:
            break
        if g.game_status not in ['Final']:
            continue

        games[g.home_team]['games'] += 1
        games[g.home_team]['home']['games'] += 1
        games[g.away_team]['games'] += 1
        games[g.away_team]['away']['games'] += 1

        games[g.home_team]['goals_for'] += g.team_scoring['home']['goals']
        games[g.home_team]['goals_against'] += g.team_scoring['away']['goals']

        games[g.away_team]['goals_for'] += g.team_scoring['away']['goals']
        games[g.away_team]['goals_against'] += g.team_scoring['home']['goals']

        games[g.home_team]['goals_diff'] = games[g.home_team]['goals_for'] - \
            games[g.home_team]['goals_against']
        games[g.away_team]['goals_diff'] = games[g.away_team]['goals_for'] - \
            games[g.away_team]['goals_against']

        if g.winner_side == 'home':
            games[g.home_team]['wins'] += 1
            games[g.home_team]['home']['wins'] += 1

            if len(g.periods) > 3:
                games[g.away_team]['otl'] += 1
                games[g.away_team]['away']['otl'] += 1
            else:
                games[g.away_team]['losses'] += 1
                games[g.away_team]['away']['losses'] += 1

        else:
            games[g.away_team]['wins'] += 1
            games[g.away_team]['away']['wins'] += 1

            if len(g.periods) > 3:
                games[g.home_team]['otl'] += 1
                games[g.home_team]['home']['otl'] += 1
            else:
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
    if by == 'nhl':
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


def get_team_details(season, team_name, to_date=None):

    team_info = get_team(team_name)
    standings = get_standings(season, team_name=team_name, to_date=to_date)

    gameplayers = gameplayer.get_gameplayers_by_team(
        season, team_name, to_date=to_date)

    all_players = {}
    stats = _init_player_stats()
    for p in gameplayers:
        if p.game_type != 'R':
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

    positions = {}
    for _, v in all_players.items():
        pos = v['bio'].get('position', "Unknown").lower()
        if pos not in positions:
            positions[pos] = []
        positions[pos].append(v)

    if 'lw' not in positions:
        return None
    for p in positions.get('lw', []):
        p['stats'].pop('goalie')
    for p in positions.get('rw', []):
        p['stats'].pop('goalie')
    for p in positions['c']:
        p['stats'].pop('goalie')
    for p in positions['d']:
        p['stats'].pop('goalie')
    for p in positions['g']:
        p['stats'].pop('skater')

    num_games = standings['games']
    if num_games == 0:
        num_games = 1

    skater_per_game_keys = [
        'hits',
        'goals',
        'assists',
        'penalty_minutes',
        'takeaways',
        'giveaways',
        'blocked'
    ]

    for k in skater_per_game_keys:
        stats['skater']['%s_per_game' % k] = round(
            stats['skater'][k] / num_games,
            2
        )

    stats['skater']['faceoff_win_percentage'] = round(
        stats['skater']['face_off_wins'] / stats['skater']['faceoff_taken'],
        3
    )

    stats['skater']['shot_percentage'] = 0
    if stats['skater']['shots'] > 0:
        stats['skater']['shot_percentage'] = round(
            stats['skater']['goals'] / stats['skater']['shots'],
            4
        )

    stats['goalie']['goals_against'] = (
        stats['goalie']['shots'] - stats['goalie']['saves']
    )
    stats['goalie']['power_play_goals_against'] = (
        stats['goalie']['power_play_shots_against'] - stats[
            'goalie']['power_play_saves']
    )
    stats['goalie']['even_strength_goals_against'] = (
        stats['goalie']['even_shots_against'] - stats[
            'goalie']['even_saves']
    )
    stats['goalie']['short_handed_goals_against'] = (
        stats['goalie']['short_handed_shots_against'] - stats[
            'goalie']['short_handed_saves']
    )

    stats['goalie']['goals_against_per_game'] = round(
        stats['goalie']['goals_against'] / num_games,
        2
    )

    stats['goalie']['save_percentage'] = 0.00
    if stats['goalie']['saves'] > 0:
        stats['goalie']['save_percentage'] = round(
            stats['goalie']['saves'] / stats['goalie']['shots'],
            3
        )
        stats['goalie']['goals_against_avg'] = round(
            stats['goalie']['goals_against'] /
            (stats['goalie']['time_on_ice'] / 60 / 60),
            2
        )

    stats['goalie']['power_play_save_percentage'] = 0.00
    if stats['goalie']['power_play_saves'] > 0:
        stats['goalie']['power_play_save_percentage'] = round(
            stats['goalie']['power_play_saves'] / stats[
                'goalie']['power_play_shots_against'],
            3
        )

    stats['goalie']['even_strength_save_percentage'] = 0.00
    if stats['goalie']['even_saves'] > 0:
        stats['goalie']['even_strength_save_percentage'] = round(
            stats['goalie']['even_saves'] / stats[
                'goalie']['even_shots_against'],
            3
        )

    stats['skater'].pop('time_on_ice')
    stats['skater'].pop('even_time_on_ice')
    stats['skater'].pop('power_play_time_on_ice')
    stats['skater'].pop('short_handed_time_on_ice')
    stats['goalie'].pop('time_on_ice')
    standings.pop('team')

    return {
        'details': team_info,
        'standings': standings,
        'players': positions,
        'team_stats': stats
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

    if player_info['bio']['position'] != 'G':
        player_info['stats'].pop('goalie')

        for _, v in player_info['seasons'].items():
            v.pop('goalie')
    else:
        player_info['stats'].pop('skater')

        for _, v in player_info['seasons'].items():
            v.pop('skater')

    return player_info


def get_all_teams(season):

    all_teams = game.get_team_names(season)
    all_teams = sorted(all_teams)

    teams = []

    for t in all_teams:
        t = get_team(t)
        teams.append(t)

    return teams


def _increment_stats(stats, gameplayer_info):
    skater_per_game_keys = [
        'hits',
        'goals',
        'assists',
        'penalty_minutes',
        'takeaways',
        'giveaways',
        'blocked'
    ]

    def convert_time(v):
        p = v.split(':')

        return (int(p[0]) * 60) + int(p[1])

    for k, v in stats['skater'].items():
        gpv = gameplayer_info['stats']['skater'].get(k, 0)

        if isinstance(gpv, str) and ':' in gpv:
            gpv = convert_time(gpv)
        v += gpv

        stats['skater'][k] = v

    for k, v in stats['goalie'].items():
        gpv = gameplayer_info['stats']['goalie'].get(k, 0)
        if isinstance(gpv, str) and ':' in gpv:
            gpv = convert_time(gpv)
        v += gpv

        stats['goalie'][k] = v

    if stats['skater']['time_on_ice'] > 0:
        stats['skater']['games_played'] += 1

        for k in skater_per_game_keys:
            stats['skater']['%s_per_game' % k] = round(
                stats['skater'][k] / stats['skater']['games_played'],
                2
            )

        stats['skater']['faceoff_win_percentage'] = 0
        if stats['skater']['faceoff_taken'] > 0:
            stats['skater']['faceoff_win_percentage'] = round(
                stats['skater']['face_off_wins'] /
                stats['skater']['faceoff_taken'],
                3
            )

        stats['skater']['shot_percentage'] = 0
        if stats['skater']['shots'] > 0:
            stats['skater']['shot_percentage'] = round(
                stats['skater']['goals'] / stats['skater']['shots'],
                4
            )

    if stats['goalie']['time_on_ice'] > 0:
        stats['goalie']['games_played'] += 1

        stats['goalie']['goals_against'] = (
            stats['goalie']['shots'] - stats['goalie']['saves']
        )
        stats['goalie']['power_play_goals_against'] = (
            stats['goalie']['power_play_shots_against'] - stats[
                'goalie']['power_play_saves']
        )
        stats['goalie']['even_strength_goals_against'] = (
            stats['goalie']['even_shots_against'] - stats[
                'goalie']['even_saves']
        )
        stats['goalie']['short_handed_goals_against'] = (
            stats['goalie']['short_handed_shots_against'] - stats[
                'goalie']['short_handed_saves']
        )

        stats['goalie']['save_percentage'] = 0.00
        if stats['goalie']['saves'] > 0:
            stats['goalie']['save_percentage'] = round(
                stats['goalie']['saves'] / stats['goalie']['shots'],
                3
            )
            stats['goalie']['goals_against_avg'] = round(
                stats['goalie']['goals_against'] / (
                    stats['goalie']['time_on_ice'] / 60 / 60),
                2
            )

        stats['goalie']['power_play_save_percentage'] = 0.00
        if stats['goalie']['power_play_saves'] > 0 and stats[
                'goalie']['power_play_shots_against']:
            stats['goalie']['power_play_save_percentage'] = round(
                stats['goalie']['power_play_saves'] / stats[
                    'goalie']['power_play_shots_against'],
                3
            )

        stats['goalie']['even_strength_save_percentage'] = 0.00
        if stats['goalie']['even_saves'] > 0 and stats[
                'goalie']['even_shots_against']:
            stats['goalie']['even_strength_save_percentage'] = round(
                stats['goalie']['even_saves'] / stats[
                    'goalie']['even_shots_against'],
                3
            )

    return stats


def _init_player_stats():

    skater_stats = {
        'games_played': 0,
        'assists': 0,
        'goals': 0,
        'shots': 0,
        'hits': 0,
        'power_play_goals': 0,
        'power_play_assists': 0,
        'penalty_minutes': 0,
        'face_off_wins': 0,
        'faceoff_taken': 0,
        'takeaways': 0,
        'giveaways': 0,
        'short_handed_goals': 0,
        'short_handed_assists': 0,
        'blocked': 0,
        'plus_minus': 0,
        'shot_percentage': 0,
        'faceoff_win_percentage': 0,
        'hits_per_game': 0,
        'goals_per_game': 0,
        'assists_per_game': 0,
        'penalty_minutes_per_game': 0,
        'takeaways_per_game': 0,
        'giveaways_per_game': 0,
        'blocked_per_game': 0,

        'even_time_on_ice': 0,
        'power_play_time_on_ice': 0,
        'short_handed_time_on_ice': 0,
        'time_on_ice': 0,
    }

    goalie_stats = {
        'games_played': 0,
        'time_on_ice': 0,
        'assists': 0,
        'goals': 0,
        'pim': 0,
        'shots': 0,
        'saves': 0,
        'power_play_saves': 0,
        'short_handed_saves': 0,
        'even_saves': 10,
        'short_handed_shots_against': 0,
        'even_shots_against': 0,
        'power_play_shots_against': 0,
        'save_percentage': 0,
        'power_play_save_percentage': 0,
        'even_strength_save_percentage': 0,
        'goals_against_avg': 0,
        'short_handed_goals_against': 0,
        'even_strength_goals_against': 0,
        'power_play_goals_against': 0
    }

    return {
        'skater': skater_stats,
        'goalie': goalie_stats,
    }
