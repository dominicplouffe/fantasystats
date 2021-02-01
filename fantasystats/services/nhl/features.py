from datetime import timedelta
from fantasystats.managers.nhl import team
from fantasystats.services.nhl import game
from fantasystats.context import logger
from fantasystats.services import search
from fantasystats.context import db

PLAYER_KEYS = [
    'games_played',
    'assists',
    'goals',
    'shots',
    'hits',
    'power_play_goals',
    'power_play_assists',
    'penalty_minutes',
    'face_off_wins',
    'faceoff_taken',
    'takeaways',
    'giveaways',
    'short_handed_goals',
    'short_handed_assists',
    'blocked',
    'plus_minus',
    'shot_percentage',
    'faceoff_win_percentage',
    'hits_per_game',
    'goals_per_game',
    'assists_per_game',
    'penalty_minutes_per_game',
    'takeaways_per_game',
    'giveaways_per_game',
    'blocked_per_game',
    'even_time_on_ice',
    'power_play_time_on_ice',
    'short_handed_time_on_ice',
    'time_on_ice',
]

GOALIE_KEYS = [
    'games_played',
    'time_on_ice',
    'assists',
    'goals',
    'pim',
    'shots',
    'saves',
    'power_play_saves',
    'short_handed_saves',
    'even_saves',
    'short_handed_shots_against',
    'even_shots_against',
    'power_play_shots_against',
    'save_percentage',
    'power_play_save_percentage',
    'even_strength_save_percentage',
    'goals_against_avg',
    'short_handed_goals_against',
    'even_strength_goals_against',
    'power_play_goals_against',
    'goals_against',
]

POS = [
    ('goalie', GOALIE_KEYS),
    ('skater', PLAYER_KEYS)
]


def generate_game_date_features(season, game_date):

    teams = team.get_teams()

    team_features = []
    max_features = {
        'skater': {},
        'goalie': {}
    }
    min_features = {
        'skater': {},
        'goalie': {}
    }
    pos = ['skater', 'goalie']

    for i, game_team in enumerate(teams):
        if game_team.conference not in [
            'Eastern',
            'Western'
        ]:
            continue
        if game_team.division == 'n/a':
            continue
        # logger.info('Features,%s' % game_team.name_search)
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

        db.nhl_features.replace_one(
            {'_id': details['_id']}, details, upsert=True)


def get_game_features(away_team, home_team, game_date, game_info=None):
    features_home = []
    features_away = []

    result_home = 0
    result_away = 0

    feature_date = game_date - timedelta(days=1)

    home_info = db.nhl_features.find_one({
        'details.team_id': home_team,
        'feature_date': feature_date
    })

    away_info = db.nhl_features.find_one({
        'details.team_id': away_team,
        'feature_date': feature_date
    })

    if home_info is None or away_info is None:
        return None

    if home_info['standings']['games'] < 20 and game_info:
        return None

    if away_info['standings']['games'] < 20 and game_info:
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
                features_home.append(0.0)
                features_away.append(0.0)
                features_home.append(0.0)
                features_away.append(0.0)
                features_home.append(0.0)
                features_away.append(0.0)
                continue

            if value_home > value_away:
                features_home.append(1.0)
                features_away.append(0.0)
            else:
                features_home.append(0.0)
                features_away.append(1.0)

            if value_home > value_away + (value_away * 0.25):
                features_home.append(1.0)
                features_away.append(0.0)
            elif value_away > value_home + (value_home * 0.25):
                features_home.append(0.0)
                features_away.append(1.0)
            else:
                features_home.append(0.0)
                features_away.append(0.0)

            if value_home > value_away + (value_away * 0.5):
                features_home.append(1.0)
                features_away.append(0.0)
            elif value_away > value_home + (value_home * 0.5):
                features_home.append(0.0)
                features_away.append(1.0)
            else:
                features_home.append(0.0)
                features_away.append(0.0)

            if value_home > value_away + (value_away * 0.75):
                features_home.append(1.0)
                features_away.append(0.0)
            elif value_away > value_home + (value_home * 0.75):
                features_home.append(0.0)
                features_away.append(1.0)
            else:
                features_home.append(0.0)
                features_away.append(0.0)

    if game_info:
        result_home = game_info.team_scoring['home'].get('goals', 0)
        result_away = game_info.team_scoring['away'].get('goals', 0)

        if result_home == 0 and result_away == 0:
            logger.info('Invalid result => %s' % game_info.game_key)
            return None

    return {
        'features_home': features_home,
        'features_away': features_away,
        'result_home': result_home,
        'result_away': result_away
    }


if __name__ == '__main__':

    seasons = [
        "20162017",
        "20172018",
        "20182019",
        "20192020",
        "20202021"
    ]

    for season in seasons:
        dates = db.nhl_game.find({'season': season}).distinct('game_date')
        dates = sorted(dates)
        for d in dates:
            logger.info(d)
            generate_game_date_features(
                season,
                d
            )
