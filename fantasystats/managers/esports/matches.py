from fantasystats.models.esports import matches
from mongoengine import DoesNotExist
from fantasystats.services import search


def insert_match(
    game_date,
    start_time,
    match_name,
    match_id,
    event_name,
    event_id,
    category,
    competitors,
    score,
    bets
):

    game_key = search.create_eports_game_key(
        event_name,
        match_name
    )

    print(game_key)

    t = get_match_by_game_key(game_key)
    if t is not None:
        t.game_date = game_date
        t.start_time = start_time
        t.match_name = match_name
        t.match_id = match_id
        t.event_name = event_name
        t.event_id = event_id
        t.category = category
        t.competitors = competitors
        t.score = score
        t.bets = bets
        t.save()
    else:
        t = matches.match(
            game_key=game_key,
            game_date=game_date,
            start_time=start_time,
            match_name=match_name,
            match_id=match_id,
            event_name=event_name,
            event_id=event_id,
            category=category,
            competitors=competitors,
            score=score,
            bets=bets
        )
        t.save()

    return t


def get_match_by_game_key(game_key):

    try:
        t = matches.match.objects.get(game_key=game_key)
        return t
    except DoesNotExist:
        return None
