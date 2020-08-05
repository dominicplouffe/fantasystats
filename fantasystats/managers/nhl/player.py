from fantasystats.models.nhl import player
from mongoengine import DoesNotExist
from fantasystats.services import search
from fantasystats.services.crawlers import nhl
from datetime import datetime


def insert_player(
    full_name,
    name,
    first_name,
    last_name,
    primary_number,
    birth_date,
    birth_city,
    birth_state,
    birth_country,
    weight,
    height,
    position,
    shoot_catch_side,
    nhl_id
):

    name_search = search.get_search_value(full_name)

    try:
        p = player.nhl_player.objects.get(name_search=name_search)
    except DoesNotExist:

        p = player.nhl_player(
            full_name=full_name,
            name=name,
            first_name=first_name,
            last_name=last_name,
            primary_number=primary_number,
            birth_date=birth_date,
            birth_city=birth_city,
            birth_state=birth_state,
            birth_country=birth_country,
            weight=weight,
            height=height,
            position=position,
            shoot_catch_side=shoot_catch_side,
            nhl_id=nhl_id,
            name_search=name_search
        )

        p.save()

    if p.player_img_on is None or (
        datetime.utcnow() - p.player_img_on
    ).days >= 7:
        img_url = nhl.get_player_thumbnail(p.nhl_id, p.full_name)
        if img_url is not None:
            p.player_img = img_url
        p.player_img_on = datetime.utcnow()
        p.save()

    return p


def get_player_by_name(name):
    name_search = search.get_search_value(name)

    try:
        p = player.nhl_player.objects.get(name_search=name_search)
        return p
    except DoesNotExist:
        return None
