from datetime import datetime, timedelta
from fantasystats.context import logger
from fantasystats.managers.nhl import fantasy
from fantasystats.managers.nhl import gameplayer
from fantasystats.services.crawlers import numberfire


def get_player_fantasy_points():
    date = datetime.utcnow() - timedelta(hours=5)
    date = datetime(date.year, date.month, date.day)

    gameplayers = gameplayer.get_gameplayer_by_date(date)

    for gameplayer_info in gameplayers:

        price = numberfire.get_fantasy_price(
            'nhl',
            gameplayer_info.player_name
        )

        logger.info('fantasy,%s,%s' % (
            gameplayer_info.player_name,
            price
        ))

        fantasy.insert_fantasy(
            gameplayer_info.gameplayer_key,
            price,
            gameplayer_info.player_name,
            date,
            gameplayer_info.game_key,
            'FanDuel'
        )


if __name__ == '__main__':
    get_player_fantasy_points()
