from fantasystats.services.crawlers import nfl


def get_schedule():

    schedule = nfl.get_schedule()
    games = []
    for game in schedule:

        game_info = nfl.get_game(game)
        games.append(game_info)


if __name__ == '__main__':

    get_schedule()
