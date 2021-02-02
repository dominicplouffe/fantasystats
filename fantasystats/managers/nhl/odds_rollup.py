from mongoengine import DoesNotExist
from fantasystats.services import search
from fantasystats.models.nhl.odds_rollup import nhl_oddsrollup


def insert_rollup(
    noline,
    spread,
    over_under,
    points,
    team_name,
    rollup_date
):

    team_id = search.get_search_value(team_name)
    rollup_id = search.create_odds_rollup_key(team_id, rollup_date)

    try:
        rollup = nhl_oddsrollup.objects.get(rollup_id=rollup_id)

        rollup.noline = noline
        rollup.spread = spread
        rollup.over_under = over_under
        rollup.points = points

        rollup.save()

    except DoesNotExist:
        rollup = nhl_oddsrollup(
            rollup_id=rollup_id,
            noline=noline,
            spread=spread,
            over_under=over_under,
            points=points,
            team_id=team_id,
            rollup_date=rollup_date
        )
        rollup.save()

    return rollup
