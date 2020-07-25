from fantasystats.models.mlb import player
from mongoengine import DoesNotExist
from fantasystats.services import search
from fantasystats.services.crawlers import mlb
from datetime import datetime, timedelta


def insert_player(
    full_name,
    name,
    first_name,
    last_name,
    middle_name,
    box_score_name,
    primary_number,
    birth_date,
    birth_city,
    birth_state,
    birth_country,
    weight,
    height,
    position,
    bat_side,
    pitch_side,
    draft_year,
    mlb_id
):

    name_search = search.get_search_value(box_score_name)

    try:
        p = player.mlb_player.objects.get(name_search=name_search)
    except DoesNotExist:

        p = player.mlb_player(
            full_name=full_name,
            name=name,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            box_score_name=box_score_name,
            primary_number=primary_number,
            birth_date=birth_date,
            birth_city=birth_city,
            birth_state=birth_state,
            birth_country=birth_country,
            weight=weight,
            height=height,
            position=position,
            bat_side=bat_side,
            pitch_side=pitch_side,
            draft_year=draft_year,
            mlb_id=mlb_id,
            name_search=name_search
        )

        p.save()

    if p.player_img_on is None or (datetime.utcnow() - p.player_img_on).days >= 7:
        img_url = mlb.get_player_thumbnail(p.box_score_name)
        if img_url is not None:
            p.player_img = img_url
        p.player_img_on = datetime.utcnow()
        p.save()

    return p


def get_player_by_name(name):
    name_search = search.get_search_value(name)

    try:
        p = player.mlb_player.objects.get(name_search=name_search)
        return p
    except DoesNotExist:
        return None
