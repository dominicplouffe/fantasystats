from mongoengine import DoesNotExist
from fantasystats.services import search
from fantasystats.models.nba.odds_rollup import mlb_oddsrollup


def insert_rollup(
    noline,
    spread,
    over_under,
    points,
    team_name,
    rollup_date,
    trends
):

    team_id = search.get_search_value(team_name)
    rollup_id = search.create_odds_rollup_key(team_id, rollup_date)

    try:
        rollup = mlb_oddsrollup.objects.get(rollup_id=rollup_id)

        rollup.noline = noline
        rollup.spread = spread
        rollup.over_under = over_under
        rollup.points = points
        rollup.trends = trends

        rollup.save()

    except DoesNotExist:
        rollup = mlb_oddsrollup(
            rollup_id=rollup_id,
            noline=noline,
            spread=spread,
            over_under=over_under,
            points=points,
            team_id=team_id,
            rollup_date=rollup_date,
            trends=trends
        )
        rollup.save()

    return rollup


def get_odds_rollup(team_name, to_date):

    team_id = search.get_search_value(team_name)
    rollup_id = search.create_odds_rollup_key(team_id, to_date)

    try:
        rollup = mlb_oddsrollup.objects.get(rollup_id=rollup_id)

        return rollup
    except DoesNotExist:
        return None
