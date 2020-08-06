import requests
from lxml import html
from fantasystats.services import search


FANTASY_URL = 'https://www.numberfire.com/%s/players/daily-fantasy/%s'


def get_fantasy_price(league, player_name):

    if league not in ['mlb', 'nhl']:
        raise ValueError('Invalid league')

    player_name = search.get_search_value(player_name)

    url = FANTASY_URL % (league, player_name)

    r = requests.get(url)
    doc = html.fromstring(r.content)

    tbody = doc.xpath('//tbody[@class="projection-table__body"]')

    if len(tbody) == 0:
        return 0.00

    price = tbody[1].xpath('.//td[@class="cost"]/text()')

    if len(price) == 0:
        return 0.00

    try:
        return float(price[0].strip().replace(',', '').replace('$', ''))
    except ValueError:
        return 0.00


if __name__ == '__main__':

    print(get_fantasy_price('mlb', 'robinson_cano'))
