from fantasystats.models.nba import player
from mongoengine import DoesNotExist
from fantasystats.services import search
from fantasystats.services.crawlers import nba
from datetime import datetime


def insert_player(
    full_name,
    name,
    first_name,
    last_name,
    name_code,
    primary_number,
    birth_date,
    birth_country,
    weight,
    height,
    position,
    draft_year,
    affiliation,
    schoolType,
    nba_id
):

    name_search = search.get_search_value(full_name)

    try:
        p = player.nba_player.objects.get(name_search=name_search)
    except DoesNotExist:

        p = player.nba_player(
            full_name=full_name,
            name=name,
            first_name=first_name,
            last_name=last_name,
            name_code=name_code,
            primary_number=primary_number,
            birth_date=birth_date,
            birth_country=birth_country,
            weight=weight,
            height=height,
            position=position,
            draft_year=draft_year,
            nba_id=nba_id,
            affiliation=affiliation,
            schoolType=schoolType,
            name_search=name_search
        )

        p.save()

    # TODO Get Player Image
    if p.player_img_on is None or (
        datetime.utcnow() - p.player_img_on
    ).days >= 7:
        img_url = nba.get_player_thumbnail(
            nba_id,
            full_name
        )
        if img_url is not None:
            p.player_img = img_url
        p.player_img_on = datetime.utcnow()
        p.save()

    return p


def get_player_by_name(name):
    name_search = search.get_search_value(name)

    try:
        p = player.nba_player.objects.get(name_search=name_search)
        return p
    except DoesNotExist:
        return None
