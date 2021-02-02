from unidecode import unidecode


def get_search_value(value):

    value = unidecode(value.lower())
    value = value.replace("'", '')
    value = value.replace("`", '')
    value = value.replace(" ", '_')
    value = value.replace(".", '')

    return value


def create_game_key(
    game_date,
    away_team,
    home_team,
    double_header,
    game_number
):

    away_name = ""
    home_name = ""

    if isinstance(away_team, str):
        away_name = get_search_value(away_team)
    else:
        away_name = away_team.name_search
    if isinstance(home_team, str):
        home_name = get_search_value(home_team)
    else:
        home_name = home_team.name_search

    return '%s-%s-%s-%s-%s' % (
        game_date.strftime('%Y-%m-%d'),
        away_name,
        home_name,
        double_header,
        game_number
    )


def create_gameplayer_key(
    game_key,
    team_name,
    player_name
):
    return '%s-%s-%s' % (
        game_key,
        get_search_value(team_name),
        get_search_value(player_name)
    )


def create_feature_key(team_name, feature_date):
    return '%s-%s' % (
        feature_date.strftime('%Y-%m-%d'),
        get_search_value(team_name),
    )


def create_odds_rollup_key(team_name, date):
    return '%s-%s' % (
        get_search_value(team_name),
        date.strftime('%Y-%m-%d')
    )
