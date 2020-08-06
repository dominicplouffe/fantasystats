from datetime import datetime, timedelta
from fantasystats.context import logger
from fantasystats.managers.nhl import fantasy
from fantasystats.managers.nhl import gameplayer, game
from fantasystats.services.crawlers import numberfire
from fantasystats.services import search


def get_player_fantasy_points():
    date = datetime.utcnow() - timedelta(hours=5)
    date = datetime(date.year, date.month, date.day)

    games = game.get_by_game_date(date)
    gameplayers = []

    for game_info in games:
        player_names = gameplayer.get_distince_gameplayer_by_team(
            game_info.season, game_info.home_team
        )

        for player_name in player_names:
            gameplayers.append({
                'player_name': player_name,
                'game_key': game_info.game_key,
                'gameplayer_key': search.create_gameplayer_key(
                    game_info.game_key,
                    game_info.home_team,
                    player_name
                )

            })

        player_names = gameplayer.get_distince_gameplayer_by_team(
            game_info.season, game_info.away_team
        )

        for player_name in player_names:
            gameplayers.append({
                'player_name': player_name,
                'game_key': game_info.game_key,
                'gameplayer_key': search.create_gameplayer_key(
                    game_info.game_key,
                    game_info.away_team,
                    player_name
                )

            })

    for gameplayer_info in gameplayers:

        price = numberfire.get_fantasy_price(
            'nhl',
            gameplayer_info['player_name']
        )

        logger.info('fantasy,%s,%s' % (
            gameplayer_info['player_name'],
            price
        ))

        fantasy.insert_fantasy(
            gameplayer_info['gameplayer_key'],
            price,
            gameplayer_info['player_name'],
            date,
            gameplayer_info['game_key'],
            'FanDuel'
        )


if __name__ == '__main__':
    get_player_fantasy_points()
