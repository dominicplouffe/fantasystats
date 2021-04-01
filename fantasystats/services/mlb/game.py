import pickle
from fantasystats import context
from datetime import datetime, timedelta
from fantasystats.services import consensus
from fantasystats.context import REDIS
from fantasystats.managers.mlb import (
    game, team, venue, player, gameplayer, fantasy, season, prediction,
    odds_rollup
)
from fantasystats.services.picks import PROVIDERS


def get_games_by_date(game_date):

    now_date = datetime.utcnow()
    now_date = datetime(now_date.year, now_date.month, now_date.day)

    if game_date >= now_date:
        all_games = game.get_by_game_date(game_date)
    else:
        all_games = [
            g for g in game.get_by_game_date(game_date)
            if g.game_status not in ['Preview', 'Scheduled']
        ]

    return [
        get_game_by_key(
            g.game_key,
            game_info=g,
            include_players=False,
            to_date=game_date,
            include_odds=True,
            include_predictions=True,
            include_injuries=False,
            standings=False,
            team_scoring=True,
        )
        for g in all_games
    ]


def get_game_by_key(
    game_key,
    game_info=None,
    include_players=False,
    include_odds=False,
    include_predictions=False,
    include_injuries=False,
    to_date=None,
    standings=False,
    team_scoring=True,
    force_query=False
):

    if not game_info:
        game_info = game.get_game_by_key(game_key)

    if game_info is None:
        return {}

    if not to_date:
        to_date = game_info.game_date

    home_team_name = game_info.home_team
    away_team_name = game_info.away_team

    game_info.home_team = get_team(
        game_info.home_team,
        standings=True,
        season=game_info.season if standings else None,
        to_date=to_date,
        force_query=force_query
    )
    game_info.away_team = get_team(
        game_info.away_team,
        standings=True,
        season=game_info.season if standings else None,
        to_date=to_date,
        force_query=force_query
    )

    if not game_info.home_team or not game_info.away_team:
        return None

    game_info.home_pitcher = get_player_bio(game_info.home_pitcher)
    game_info.away_pitcher = get_player_bio(game_info.away_pitcher)
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
        odds = context.db.mlb_odds.find_one({
            '_id': game_key
        })

        if odds:
            odds.pop('_id')
            odds.pop('game_key')

            odds = consensus.find_best_odds(odds)

            if odds:
                game_info['odds'] = {
                    'sites': odds,
                    'consensus': consensus.get_odds_consensus(odds)
                }

    if include_predictions and include_odds:
        preds = prediction.get_prediction_by_game_key(game_key)

        con_data = consensus.get_prediction_consensus(
            preds,
            game_info.get('odds', {}).get('consensus', [])
        )

        pred_sites = []
        for p in preds:
            con_data['picks'].get(p.provider, {})['winner'] = p.winner
            pred_sites.append({
                'provider': PROVIDERS.get(p.provider, p.provider),
                'game_url': p.game_url,
                'icon': 'https://%s/favicon.ico' % p.game_url.split('/')[2],
                'predictions': p.payload,
                'picks': con_data['picks'].get(p.provider, {})
            })

        game_info['predictions'] = {
            'sites': pred_sites,
            'consensus': con_data['predictions']
        }

        if 'odds' in game_info:
            game_info['best_bets'] = consensus.get_best_bets(
                game_info['predictions']['sites'],
                game_info['odds']['sites']
            )

    if 'broadcasters' not in game_info:
        game_info['broadcasters'] = []

    game_info['start_time'] += timedelta(hours=5)
    game_info['league'] = 'mlb'

    if not team_scoring and 'team_scoring' in game_info:
        game_info.pop('team_scoring')

    return game_info


def get_team(
    team_name, standings=False, season=None, to_date=None, force_query=False
):
    if standings and not season:
        raise ValueError(
            'season must be added as an argument is standings is passed')

    if season and not standings:
        raise ValueError(
            'standings must be added as an argument is season is passed')

    key = 'a%s-%s-%s-%s' % (
        team_name, standings, season, to_date
    )

    data = REDIS.get(key)

    if data and not force_query:
        return pickle.loads(data)

    standings_res = None
    team_info = team.get_team_by_name(team_name)

    if not team_info:
        return team_info

    if standings:
        standings_res = get_standings(
            season, team_name=team_info.name_search, to_date=to_date)
        try:
            standings_res.pop('team')
        except TypeError:
            return None

    record = None
    if to_date and standings:
        rollup_stats = odds_rollup.get_odds_rollup(
            team_info.name_search, to_date
        )

        if rollup_stats:
            if rollup_stats.trends:
                rollup_stats.trends.reverse()

            record = {
                'noline': rollup_stats.noline,
                'spread': rollup_stats.spread,
                'over_under': rollup_stats.over_under,
                'points': rollup_stats.points,
                'trends': rollup_stats.trends
            }

    data = {
        'full_name': team_info.full_name,
        'name': team_info.name,
        'location_name': team_info.location_name,
        'league': team_info.league,
        'division': team_info.division,
        'venue': get_venue(team_info.venue),
        'abbr': team_info.abbr,
        'team_id': team_info.name_search,
        'color1': team_info.color1,
        'color2': team_info.color2,
        'color3': team_info.color3,
        'logo': 'https://fantasydataobj.s3.us-east-2.amazonaws.com'
                '/mlb/teams/%s.png' % (
            team_info.name_search
        ),
        'standings': standings_res
    }

    if record:
        data['record'] = record

    REDIS.set(key, pickle.dumps(data), 3600)

    return data


def get_versus(season, away_team, home_team):

    return {
        'home': get_team_details(season, home_team),
        'away': get_team_details(season, away_team)
    }


def get_venue(venue_name):

    venue_info = venue.get_venue_by_name(venue_name)

    if not venue_info:
        return {
            'venue_name': 'n/a'
        }

    return {
        'venue_name': venue_info['name']
    }


def get_player_bio(player_name):

    player_info = player.get_player_by_name(player_name)

    if not player_info:
        return {}

    return {
        'name': player_info.box_score_name,
        'primary_number': player_info.primary_number,
        'position': player_info.position,
        'birth_date': player_info.birth_date,
        'birth_country': player_info.birth_country,
        'bat_side': player_info.bat_side,
        'pitch_side:': player_info.pitch_side,
        'draft_year': player_info.draft_year,
        'player_id': player_info.name_search,
        'headshot': 'https://fantasydataobj.s3.us-east-2.amazonaws.com'
                    '/mlb/players/%s' % player_info.player_img
    }


def get_game_players(game_key, home_team, away_team):

    gameplayers = gameplayer.get_gameplayers_by_game_key(game_key)

    all_players = {
        'home': {
            'batters': [],
            'pitchers': [],
            'fielders': []
        },
        'away': {
            'batters': [],
            'pitchers': [],
            'fielders': []
        },
    }

    for p in gameplayers:

        player_info = get_player_bio(p.player_name)
        if not player_info:
            continue
        batting = None
        fielding = None
        pitching = None

        fantasy_info = fantasy.get_fantasy_by_gameplayer_key(
            p.gameplayer_key
        )
        fantasy_data = {'FanDuel': {'price': 0}}
        if fantasy_info:
            fantasy_data['FanDuel'] = {'price': fantasy_info.price}
        player_info['fantasy'] = fantasy_data

        if p.is_batter:
            batting = p.stats['batting']
            batting['bio'] = player_info
            batting['player_name'] = player_info['name']
            batting['player_id'] = p['player_name']
            if p.team_name == home_team:
                all_players['home']['batters'].append(batting)
            else:
                all_players['away']['batters'].append(batting)
        if p.is_pitcher:
            pitching = p.stats['pitching']
            pitching['bio'] = player_info
            pitching['player_name'] = player_info['name']
            pitching['player_id'] = p['player_name']
            if p.team_name == home_team:
                all_players['home']['pitchers'].append(pitching)
            else:
                all_players['away']['pitchers'].append(pitching)
        if p.is_fielder:
            fielding = p.stats['fielding']
            fielding['bio'] = player_info
            fielding['player_name'] = player_info['name']
            fielding['player_id'] = p['player_name']
            if p.team_name == home_team:
                all_players['home']['fielders'].append(fielding)
            else:
                all_players['away']['fielders'].append(fielding)

    all_players['home']['batters'] = sorted(
        all_players['home']['batters'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )
    all_players['home']['pitchers'] = sorted(
        all_players['home']['pitchers'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )
    all_players['home']['fielders'] = sorted(
        all_players['home']['fielders'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )

    all_players['away']['batters'] = sorted(
        all_players['away']['batters'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )
    all_players['away']['pitchers'] = sorted(
        all_players['away']['pitchers'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )
    all_players['away']['fielders'] = sorted(
        all_players['away']['fielders'],
        key=lambda x: -x['bio']['fantasy']['FanDuel']['price']
    )
    return all_players


def get_standings(
    season, team_name=None, by='mlb', to_date=None, force_query=False
):

    if by not in ['league', 'mlb', 'division']:
        raise ValueError

    all_games = game.get_games_by_season(season, team_name=team_name)

    games = {}

    for g in all_games:

        if g.game_type != 'R':
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
                'runs_for': 0,
                'runs_against': 0,
                'runs_diff': 0,
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
                'runs_for': 0,
                'runs_against': 0,
                'runs_diff': 0,
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
        if g.game_status not in ['F', 'FR']:
            continue

        games[g.home_team]['games'] += 1
        games[g.home_team]['home']['games'] += 1
        games[g.away_team]['games'] += 1
        games[g.away_team]['away']['games'] += 1

        games[g.home_team]['runs_for'] += g.team_scoring['home']['runs']
        games[g.home_team]['runs_against'] += g.team_scoring['away']['runs']

        games[g.away_team]['runs_for'] += g.team_scoring['away']['runs']
        games[g.away_team]['runs_against'] += g.team_scoring['home']['runs']

        games[g.home_team]['runs_diff'] = games[g.home_team]['runs_for'] - \
            games[g.home_team]['runs_against']
        games[g.away_team]['runs_diff'] = games[g.away_team]['runs_for'] - \
            games[g.away_team]['runs_against']

        if g.winner_side == 'home':
            games[g.home_team]['wins'] += 1
            games[g.away_team]['losses'] += 1

            games[g.home_team]['home']['wins'] += 1
            games[g.away_team]['away']['losses'] += 1
        else:
            games[g.home_team]['losses'] += 1
            games[g.away_team]['wins'] += 1

            games[g.home_team]['home']['losses'] += 1
            games[g.away_team]['away']['wins'] += 1

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
    if by == 'mlb':
        return games
    elif by == 'league':
        leagues = {}
        for g in games:
            if g['team']['conference'] not in leagues:
                leagues[g['team']['conference']] = []
            leagues[g['team']['conference']].append(g)

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

            player_info = get_player_bio(p.player_name)
            fantasy_info = fantasy.get_fantansy_by_player_name(
                p.player_name
            )
            fantasy_data = {'FanDuel': {'price': 0}}
            if len(fantasy_info) > 0:
                fantasy_data['FanDuel'] = {'price': fantasy_info[0].price}
            player_info['fantasy'] = fantasy_data

            all_players[p.player_name] = {
                'bio': player_info,
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

    if 'infielder' not in positions:
        return None
    for p in positions['infielder']:
        p['stats'].pop('pitching')
    for p in positions['outfielder']:
        p['stats'].pop('pitching')
    for p in positions['catcher']:
        p['stats'].pop('pitching')

    num_games = standings['games']
    if num_games == 0:
        num_games = 1
    stats['fielding']['errors_per_game'] = round(
        stats['fielding']['errors'] / num_games,
        2
    )
    stats['pitching']['avg_against'] = round(
        stats['pitching']['hits'] / stats['pitching']['at_bats'],
        3
    )
    stats['pitching']['obp_against'] = round(
        (
            stats['pitching']['hits'] + stats['pitching'][
                'base_on_balls'
            ] + stats['pitching']['hit_batsmen']
        ) / (
            stats['pitching']['hits'] + stats['pitching']['base_on_balls'] +
            stats['pitching']['hit_batsmen'] + stats['pitching']['sac_flies']
        ),
        3
    )

    stats['batting']['stolen_bases_per_game'] = round(
        stats['batting']['stolen_bases'] / num_games,
        2
    )
    stats['batting']['home_runs_per_game'] = round(
        stats['batting']['home_runs'] / num_games,
        2
    )
    stats['batting']['runs_per_game'] = round(
        stats['batting']['runs'] / num_games,
        2
    )

    stats['batting']['obps'] = round(
        stats['batting']['obp'] + stats['batting']['slug'],
        2
    )

    stats['batting'].pop('games_played')
    stats['pitching'].pop('games_played')
    stats['pitching'].pop('games_pitched')
    stats['pitching'].pop('games_finished')
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

    if player_info['bio']['position'] != 'Pitcher':
        player_info['stats'].pop('pitching')

        for _, v in player_info['seasons'].items():
            v.pop('pitching')

    return player_info


def get_all_teams(season):

    all_teams = game.get_team_names(season)
    all_teams = sorted(all_teams)

    teams = []

    for t in all_teams:
        if '_winner' in t:
            continue
        if '_runner' in t:
            continue
        if '/' in t:
            continue
        if 'wild_card' in t:
            continue
        t = get_team(t)
        if t['league'] not in [
            'American League',
            'National League'
        ]:
            continue
        if t['division'] == 'n/a':
            continue

        teams.append(t)

    return teams


def get_game_by_team(season, team_name):

    all_games = game.get_games_by_season(season, team_name=team_name)

    all_games = [
        get_game_by_key(
            g.game_key,
            game_info=g,
            include_players=False,
            standings=True,
            include_odds=True,
            include_predictions=True,
            include_injuries=False
        )
        for g in all_games
    ]

    return [g for g in all_games if g]


def _increment_stats(stats, gameplayer_info):

    for k, v in stats['batting'].items():
        gpv = gameplayer_info['stats']['batting'].get(k, 0)
        v += gpv

        stats['batting'][k] = v

    for k, v in stats['pitching'].items():
        gpv = gameplayer_info['stats']['pitching'].get(k, 0)
        v += gpv

        stats['pitching'][k] = v

    for k, v in stats['fielding'].items():
        gpv = gameplayer_info['stats']['fielding'].get(k, 0)
        v += gpv

        stats['fielding'][k] = v

    if stats['batting']['at_bats'] > 0:
        hits = stats['batting']['hits']
        at_bats = stats['batting']['at_bats']
        doubles = stats['batting']['doubles']
        triples = stats['batting']['triples']
        homeruns = stats['batting']['home_runs']
        walks = stats['batting']['base_on_balls']
        hit_by_pitch = stats['batting']['hit_by_pitch']
        sac_flies = stats['batting']['sac_flies']
        singles = hits - doubles - triples - homeruns

        stats['batting']['singles'] = singles
        stats['batting']['avg'] = round(hits / at_bats, 3)
        stats['batting']['slug'] = round(
            ((singles) + (doubles * 2) + (triples * 3) + (
                homeruns * 4
            )) / at_bats,
            3
        )
        stats['batting']['obp'] = round(
            (hits + walks + hit_by_pitch) / (
                at_bats + walks + hit_by_pitch + sac_flies
            ),
            3
        )
        stats['batting']['obp'] = stats['batting']['slug'] + \
            stats['batting']['obp']

    if stats['pitching']['innings_pitched'] > 0:
        at_bats = stats['pitching']['at_bats']
        hits = stats['pitching']['hits']
        at_bats = stats['pitching']['at_bats']
        doubles = stats['pitching']['doubles']
        triples = stats['pitching']['triples']
        homeruns = stats['pitching']['home_runs']
        walks = stats['pitching']['base_on_balls']
        hit_by_pitch = stats['pitching']['hit_by_pitch']
        strike_outs = stats['pitching']['strike_outs']
        sac_flies = stats['pitching']['sac_flies']
        pitches_thrown = stats['pitching']['pitches_thrown']
        strikes = stats['pitching']['strikes']
        balls = stats['pitching']['balls']

        singles = hits - doubles - triples - homeruns

        innings = stats['pitching']['innings_pitched']
        stats['pitching']['era'] = round(
            (9 * stats['pitching']['earned_runs']) /
            innings,
            3
        )
        if at_bats == 0:
            at_bats = 1
            pitches_thrown = 1
            put_outs = 1

        stats['pitching']['avg'] = round(hits / at_bats, 3)

        stats['pitching']['slug'] = round(
            ((singles) + (doubles * 2) + (triples * 3) + (
                homeruns * 4
            )) / at_bats,
            3
        )
        stats['pitching']['obp'] = round(
            (hits + walks + hit_by_pitch) / (
                at_bats + walks + hit_by_pitch + sac_flies
            ),
            3
        )
        stats['pitching']['obp'] = stats['pitching']['slug'] + \
            stats['pitching']['obp']
        stats['pitching']['strike_out_per'] = round(
            strike_outs / at_bats,
            3
        )
        stats['pitching']['strike_per'] = round(
            strikes / pitches_thrown,
            3
        )
        stats['pitching']['ball_per'] = round(
            balls / pitches_thrown,
            3
        )

    if stats['fielding']['put_outs'] > 0:
        put_outs = stats['fielding']['put_outs']
        assists = stats['fielding']['assists']
        errors = stats['fielding']['errors']

        stats['fielding']['fielding_per'] = round(
            (put_outs + assists) / (
                put_outs + assists + errors
            ),
            3
        )
    return stats


def _init_player_stats():

    pitching_stats = {
        'games_played': 0,
        'games_started': 0,
        'fly_outs': 0,
        'ground_outs': 0,
        'air_outs': 0,
        'runs': 0,
        'doubles': 0,
        'triples': 0,
        'home_runs': 0,
        'strike_outs': 0,
        'base_on_balls': 0,
        'intentional_walks': 0,
        'hits': 0,
        'hit_by_pitch': 0,
        'at_bats': 0,
        'caught_stealing': 0,
        'stolen_bases': 0,
        'number_of_pitches': 0,
        'innings_pitched': 0,
        'wins': 0,
        'losses': 0,
        'saves': 0,
        'save_opportunities': 0,
        'holds': 0,
        'blown_saves': 0,
        'earned_runs': 0,
        'batters_faced': 0,
        'outs': 0,
        'games_pitched': 0,
        'complete_games': 0,
        'shutouts': 0,
        'pitches_thrown': 0,
        'balls': 0,
        'strikes': 0,
        'hit_batsmen': 0,
        'balks': 0,
        'wild_pitches': 0,
        'pickoffs': 0,
        'rbi': 0,
        'games_finished': 0,
        'inherited_runners': 0,
        'inherited_runners_scored': 0,
        'catchers_interference': 0,
        'sac_bunts': 0,
        'sac_flies': 0
    }

    fielding_stats = {
        'assists': 0,
        'put_outs': 0,
        'errors': 0,
        'chances': 0,
        'caught_stealing': 0,
        'passed_ball': 0,
        'stolen_bases': 0,
        'pickoffs': 0
    }

    batting_stats = {
        'games_played': 0,
        'fly_outs': 0,
        'ground_outs': 0,
        'runs': 0,
        'doubles': 0,
        'triples': 0,
        'home_runs': 0,
        'strike_outs': 0,
        'base_on_balls': 0,
        'intentional_walks': 0,
        'hits': 0,
        'hit_by_pitch': 0,
        'at_bats': 0,
        'caught_stealing': 0,
        'stolen_bases': 0,
        'ground_into_double_play': 0,
        'ground_into_triple_play': 0,
        'plate_appearances': 0,
        'total_bases': 0,
        'rbi': 0,
        'left_on_base': 0,
        'sac_bunts': 0,
        'sac_flies': 0,
        'catchers_interference': 0,
        'pickoffs': 0,
    }

    return {
        'batting': batting_stats,
        'fielding': fielding_stats,
        'pitching': pitching_stats
    }


def get_seasons():

    return [s for s in season.get_seasons()]
