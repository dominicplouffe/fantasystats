import requests
from lxml import html
from fantasystats.services import search


FANTASY_URL = 'https://www.numberfire.com/%s/players/daily-fantasy/%s'
SEARCH_URL = 'https://www.numberfire.com/search?term=%s'


def get_fantasy_price(league, player_name, do_search=False):

    if league not in ['mlb', 'nhl', 'nba']:
        raise ValueError('Invalid league')

    if do_search:
        player_name = player_name.replace('_',  ' ')
        url = SEARCH_URL % player_name

        search_r = requests.get(url).json()
        if len(search_r) == 0:
            return 0.00

        url = FANTASY_URL % (league, search_r[0]['slug'])

    else:
        player_name = search.get_search_value(player_name)
        url = FANTASY_URL % (league, player_name)

    r = requests.get(url)
    doc = html.fromstring(r.content)

    tbody = doc.xpath('//tbody[@class="projection-table__body"]')

    if len(tbody) == 0:
        if not do_search:
            return get_fantasy_price(league, player_name, do_search=True)

        return 0.00

    price = tbody[1].xpath('.//td[@class="cost"]/text()')

    if len(price) == 0:
        return 0.00

    try:
        return float(price[0].strip().replace(',', '').replace('$', ''))
    except ValueError:
        return 0.00


if __name__ == '__main__':

    print(get_fantasy_price('nba', 'Jerami Grant'))
