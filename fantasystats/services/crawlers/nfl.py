import re
import json
import requests
from lxml import html
from urllib.parse import quote_plus
from datetime import datetime, timedelta
from fantasystats.services.crawlers.mappings import HEADERS

SEASON = 2020
URL_JSON = '{"Name":"Schedules","Module":{"seasonFromUrl":%s,' \
    '"SeasonType":"%s%s","WeekFromUrl":%s,"HeaderCountryCode":"CA"' \
    ',"PreSeasonPlacement":0,"RegularSeasonPlacement":0,"PostSeason' \
    'Placement":0,"TimeZoneID":"America/Toronto"}}'
URL = 'https://www.nfl.com/api/lazy/load?json=%s'
SEASON_TYPE = ['REG', 'POST']
WEEKS_PER_SEASON = {
    'REG': 16,
    'POST': 4
}
BASE_GAME_URL = 'https://www.nfl.com/games/%s'
BEARER_HEADERS = {
    'authority': 'api.nfl.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'sec-ch-ua-mobile': '?0',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRJZCI6ImU1MzVjN2MwLTgxN2YtNDc3Ni04OTkwLTU2NTU2ZjhiMTkyOCIsImRtYUNvZGUiOiI4MzkiLCJmb3JtRmFjdG9yIjoiREVTS1RPUCIsImlzcyI6Ik5GTCIsImRldmljZUlkIjoiYzQ3N2M5OTUtOGRhMi00YzFkLThkYzYtYjM2YzQwMTUzM2RjIiwicGxhdGZvcm0iOiJERVNLVE9QIiwicHJvZHVjdE5hbWUiOiJXRUIiLCJjb3VudHJ5Q29kZSI6IlVTIiwicGxhbnMiOlt7InNvdXJjZSI6Ik5GTCIsInBsYW4iOiJmcmVlIiwidHJpYWwiOiJmYWxzZSIsInN0YXR1cyI6IkFDVElWRSIsImV4cGlyYXRpb25EYXRlIjoiMjAyMi0wNi0yOCJ9XSwiY2VsbHVsYXIiOmZhbHNlLCJicm93c2VyIjoiQ2hyb21lIiwiRGlzcGxheU5hbWUiOiJXRUJfREVTS1RPUF9ERVNLVE9QIiwibHVyYUFwcEtleSI6IlNaczU3ZEJHUnhiTDcyOGxWcDdEWVEiLCJleHAiOjE2MjQ4ODI3MDQsIk5vdGVzIjoiIn0.Uom4rB3dlJhoXBxmlQeem4QODn6r3Vte7Xu2_ZpWo2Q',
    'accept': '*/*',
    'origin': 'https://www.nfl.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.nfl.com/',
    'accept-language': 'en-US,en;q=0.9',
    'x-authorization': '5d4f7dea9d93c919b2e49fe1',
}


def get_schedule():
    week = 1

    games = []

    for st in SEASON_TYPE:
        for week in range(1, WEEKS_PER_SEASON[st] + 1):

            j = URL_JSON % (
                SEASON,
                st,
                week,
                week
            )

            url = URL % quote_plus(j)
            content = requests.get(url).content
            doc = html.fromstring(content)

            sections = doc.xpath(
                '//section[contains(@class, "nfl-o-matchup-group")]'
            )
            for section in sections:
                game_date = section.xpath(
                    './/h2[@class="d3-o-section-title"]/text()'
                )[0]
                if 'Games not yet scheduled' in game_date:
                    continue
                game_date = '%s %s' % (game_date, SEASON)
                game_date = game_date.replace('st ', ' ')
                game_date = game_date.replace('nd ', ' ')
                game_date = game_date.replace('rd ', ' ')
                game_date = game_date.replace('th ', ' ')
                game_date = datetime.strptime(
                    game_date,
                    '%A, %B %d %Y'
                )
                if game_date.month in [1, 2]:
                    game_date += timedelta(days=365)

                game_id = section.xpath('.//a/@href')[0].split('/')[2]
                team_abbr = section.xpath(
                    './/span[@class="nfl-c-matchup-strip__team-abbreviation"]/text()'
                )
                team_names = section.xpath(
                    './/span[@class="nfl-c-matchup-strip__team-fullname"]/text()'
                )

                game = {
                    'week': week,
                    'game_type': st,
                    'game_date': game_date,
                    'game_id': game_id,
                    'away_team_abbr': team_abbr[0].strip(),
                    'away_team_name': team_names[0].strip(),
                    'home_team_abbr': team_abbr[1].strip(),
                    'home_team_name': team_names[1].strip(),
                    'season': SEASON,
                    'periods': 4
                }
                games.append(game)

            return games

    return games


def get_game(game_info):

    url = BASE_GAME_URL % game_info['game_id']
    s = requests.session()
    s.headers = HEADERS
    res = s.get(url)

    content = res.content
    doc = html.fromstring(content)

    game_hash = re.findall("gameID = '([^']+)'", content.decode('utf-8'))[0]
    print(game_hash)

    s.headers = BEARER_HEADERS

    res = s.get(
        'https://api.nfl.com/football/v2/games/%s?withExternalIds=true' % (
            game_hash
        )
    )
    content = res.content.decode('utf-8')
    print(content)
    game_data = json.loads(content)
    location = game_data.get('venue', {}).get('name', 'n/a')
    status = game_data['status']
    start_time = datetime.strptime(
        game_data['time'],
        '%Y-%m-%dT%H:%M:%SZ'
    )
    broadcasters = game_data['broadcastInfo']['homeNetworkChannels']
    game_info['venue'] = location
    game_info['game_status'] = status
    game_info['start_time'] = start_time
    game_info['broadcasters'] = broadcasters
    game_info['game_id'] = game_hash

    get_player_info(s, game_info)

    return game_info


def get_player_info(s, game_info):

    query = 'query{viewer{playerGameStats(first:200,game_id:"%s"){edges{cursor node{createdDate game{id}gameStats{defensiveAssists defensiveInterceptions defensiveInterceptionsYards defensiveForcedFumble defensivePassesDefensed defensiveSacks defensiveSafeties defensiveSoloTackles defensiveTotalTackles defensiveTacklesForALoss touchdownsDefense fumblesLost fumblesTotal kickReturns kickReturnsLong kickReturnsTouchdowns kickReturnsYards kickingFgAtt kickingFgLong kickingFgMade kickingXkAtt kickingXkMade passingAttempts passingCompletions passingTouchdowns passingYards passingInterceptions puntReturns puntingAverageYards puntingLong puntingPunts puntingPuntsInside20 receivingReceptions receivingTarget receivingTouchdowns receivingYards rushingAttempts rushingAverageYards rushingTouchdowns rushingYards kickoffReturnsTouchdowns kickoffReturnsYards puntReturnsLong opponentFumbleRecovery totalPointsScored kickReturnsAverageYards puntReturnsAverageYards puntReturnsTouchdowns}id lastModifiedDate player{position jerseyNumber currentTeam{abbreviation nickName}person{firstName lastName displayName headshot{url}}}season{id}week{id}}}}}' % game_info[
        'game_id']

    print(query)
    url = 'https://api.nfl.com/v3/shield/?query=%s&variables=null' % (
        quote_plus(query)
    )

    s.headers = BEARER_HEADERS
    res = s.get(url)

    player_data = json.loads(res.content.decode('utf-8'))
    print(player_data.keys())
    print(player_data)

    for p in player_data['data']['viewer']['playerGameStats']['edges']:

        print(p['node']['player'])


if __name__ == '__main__':
    # get_schedule()
    get_game({
        'game_id': 'texans-at-chiefs-2020-reg-1'
    })
