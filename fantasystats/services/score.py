def get_score(
    over_under_points,
    over_under_side,
    home_team,
    away_team,
    points_to,
    points_to_give
):
    home_score = 0
    away_score = 0

    total_score = over_under_points
    if over_under_side == "U":
        total_score = total_score - 1.0
    else:
        total_score = total_score + 1.0

    if points_to == home_team:
        home_score += points_to_give
        total_score -= points_to_give
    else:
        away_score += points_to_give
        total_score -= points_to_give

    remaining_points = total_score / 2.0
    home_score += remaining_points
    away_score += remaining_points

    if home_score < 1:
        home_score = 1.0
    if away_score < 1:
        away_score = 1.0

    return home_score, away_score


def get_score_from_odds(odds, home_team, away_team):

    scores = {}

    for book, odd in odds.items():
        try:
            over_under_points = float(odd['over_under']['under']['points'])

            if over_under_points == 0:
                scores[book] = {
                    'home': None,
                    'away': None
                }
                continue
            if float(odd['spread']['away']['spread']) == 0:
                scores[book] = {
                    'home': None,
                    'away': None
                }
                continue
            if float(odd['spread']['away']['odds']) == 0:
                scores[book] = {
                    'home': None,
                    'away': None
                }
                continue

            over_under_side = 'under'
            if float(
                odd['over_under']['over']['points']
            ) < over_under_points:
                over_under_side = 'over'

            points_to = home_team
            points_to_give = float(
                odd['spread']['home']['spread']
            )

            if float(odd['spread']['away']['spread']) > 0:
                points_to = away_team
                points_to_give = float(
                    odd['spread']['home']['spread']
                )

            home_score, away_score = get_score(
                over_under_points,
                over_under_side,
                home_team,
                away_team,
                points_to,
                points_to_give
            )

            scores[book] = {
                'home': home_score,
                'away': away_score
            }
        except ValueError:
            scores[book] = {
                'home': None,
                'away': None
            }
            continue

    return scores
