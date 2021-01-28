from datetime import timedelta
from fantasystats.managers.mlb import team
from fantasystats.services.mlb import game
from fantasystats.context import logger
from fantasystats.services import search
from fantasystats.context import db

BATTING_KEYS = [
    'fly_outs',
    'ground_outs',
    'runs',
    'doubles',
    'triples',
    'home_runs',
    'strike_outs',
    'base_on_balls',
    'intentional_walks',
    'hits',
    'hit_by_pitch',
    'at_bats',
    'caught_stealing',
    'stolen_bases',
    'ground_into_double_play',
    'ground_into_triple_play',
    'plate_appearances',
    'total_bases',
    'rbi',
    'left_on_base',
    'sac_bunts',
    'sac_flies',
    'catchers_interference',
    'pickoffs',
    'singles',
    'avg',
    'slug',
    'obp',
    'stolen_bases_per_game',
    'home_runs_per_game',
    'runs_per_game',
    'obps'
]

PITCHING_KEYS = [
    'games_started',
    'fly_outs',
    'ground_outs',
    'air_outs',
    'runs',
    'doubles',
    'triples',
    'home_runs',
    'strike_outs',
    'base_on_balls',
    'intentional_walks',
    'hits',
    'hit_by_pitch',
    'at_bats',
    'caught_stealing',
    'stolen_bases',
    'number_of_pitches',
    'innings_pitched',
    'wins',
    'losses',
    'saves',
    'save_opportunities',
    'holds',
    'blown_saves',
    'earned_runs',
    'batters_faced',
    'outs',
    'complete_games',
    'shutouts',
    'pitches_thrown',
    'balls',
    'strikes',
    'hit_batsmen',
    'balks',
    'wild_pitches',
    'pickoffs',
    'rbi',
    'inherited_runners',
    'inherited_runners_scored',
    'catchers_interference',
    'sac_bunts',
    'sac_flies',
    'era',
    'avg',
    'slug',
    'obp',
    'strike_out_per',
    'strike_per',
    'ball_per',
    'avg_against',
    'obp_against'
]

FIELDING_KEYS = [
    'assists',
    'put_outs',
    'errors',
    'chances',
    'caught_stealing',
    'passed_ball',
    'stolen_bases',
    'pickoffs',
    'fielding_per',
    'errors_per_game'
]

POS = [
    ('batting', BATTING_KEYS),
    ('fielding', FIELDING_KEYS),
    ('pitching', PITCHING_KEYS)
]


def generate_game_date_features(season, game_date):

    teams = team.get_teams()

    team_features = []
    max_features = {
        'pitching': {},
        'batting': {},
        'fielding': {}
    }
    min_features = {
        'pitching': {},
        'batting': {},
        'fielding': {}
    }
    pos = ['fielding', 'batting', 'pitching']

    for i, game_team in enumerate(teams):
        if game_team.league not in ['American League', 'National League']:
            continue
        if game_team.division == 'n/a':
            continue
        logger.info('Features,%s' % game_team.name_search)
        details = game.get_team_details(
            season, game_team.name_search, to_date=game_date)

        if details is None:
            continue
        details['index'] = {}
        for p in pos:
            details['index'][p] = {}

            for k, v in details['team_stats'][p].items():
                details['index'][p][k] = 0
                if k not in max_features[p]:
                    max_features[p][k] = v
                elif v > max_features[p][k]:
                    max_features[p][k] = v
                if k not in min_features[p]:
                    min_features[p][k] = v
                elif v < min_features[p][k]:
                    min_features[p][k] = v

        details['_id'] = search.create_feature_key(
            game_team.name_search, game_date)
        details['feature_date'] = game_date

        team_features.append(details)

    for details in team_features:
        for p in pos:
            for k, v in details['team_stats'][p].items():
                if max_features[p][k] - min_features[p][k] == 0:
                    details['index'][p][k] = 0.00
                else:
                    details['index'][p][k] = (
                        v - min_features[p][k]) / (
                            max_features[p][k] - min_features[p][k]
                    )

        db.mlb_features.replace_one(
            {'_id': details['_id']}, details, upsert=True)


def get_game_features(away_team, home_team, game_date, game_info=None):
    features_home = []
    features_away = []

    result_home = {}
    result_away = {}

    feature_date = game_date - timedelta(days=1)

    home_info = db.mlb_features.find_one({
        'details.team_id': home_team,
        'feature_date': feature_date
    })

    away_info = db.mlb_features.find_one({
        'details.team_id': away_team,
        'feature_date': feature_date
    })

    if home_info is None or away_info is None:
        return None

    if home_info['standings']['games'] < 20:
        return None

    if away_info['standings']['games'] < 20:
        return None

    cnt = 0
    for p, keys in POS:
        for b in keys:
            cnt += 1
            value_home = home_info['index'][p].get(b, 0)
            value_away = away_info['index'][p].get(b, 0)
            if value_home == 0 and value_away == 0:
                features_home.append(0.0)
                features_away.append(0.0)
                continue

            if value_home > value_away:
                features_home.append(1.0)
                features_away.append(0.0)
            else:
                features_home.append(0.0)
                features_away.append(1.0)

    if game_info:
        home_hits = game_info.team_scoring['home'].get('hits', 0)
        home_runs = game_info.team_scoring['home'].get('runs', 0)
        home_errors = game_info.team_scoring['home'].get('errors', 0)
        home_lob = game_info.team_scoring['home'].get('left_on_base', 0)

        away_hits = game_info.team_scoring['away'].get('hits', 0)
        away_runs = game_info.team_scoring['away'].get('runs', 0)
        away_errors = game_info.team_scoring['away'].get('errors', 0)
        away_lob = game_info.team_scoring['away'].get('left_on_base', 0)

        result_home['A'] = (
            (home_runs * 10) + (home_hits * 10) - (home_errors * 5) - (
                home_lob * 5
            )
        )
        result_home['B'] = (home_runs * 10) + (home_hits * 10)
        result_home['C'] = (home_runs * 100) + (home_hits * 100)
        result_home['D'] = home_hits
        result_home['E'] = home_runs

        result_away['A'] = (
            (away_runs * 10) + (away_hits * 10) - (away_errors * 5) - (
                away_lob * 5
            )
        )
        result_away['B'] = (away_runs * 10) + (away_hits * 10)
        result_away['C'] = (away_runs * 100) + (away_hits * 100)
        result_away['D'] = away_hits
        result_away['E'] = away_runs

        if result_home == 0 and result_away == 0:
            logger.info('Invalid result')
            return None

        # result_home = home_runs + home_hits
        # result_away = away_runs + away_hits

    return {
        'features_home': features_home,
        'features_away': features_away,
        'result_home': result_home,
        'result_away': result_away
    }


if __name__ == '__main__':

    season = '2020'
    dates = db.mlb_game.find({'season': season}).distinct('game_date')
    dates = sorted(dates)
    for d in dates:
        logger.info(d)
        generate_game_date_features(
            season,
            d
        )
