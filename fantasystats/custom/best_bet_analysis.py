import requests
from datetime import datetime, timedelta

start_date = datetime(2021, 2, 5)

LEAGUES = ['nba']
API_URL = 'https://api.bettingnews.com/nba/games/date/%s'


def calc_best_bets(d, points_key):
    url = API_URL % d.strftime('%Y-%m-%d')
    print(url)

    res = requests.get(url).json()

    results = {
        'num_games': 0,
        'money_line': {
            'win': 0,
            'loss': 0,
            'push': 0
        },
        'over_under': {
            'win': 0,
            'loss': 0,
            'push': 0
        },
        'spread': {
            'win': 0,
            'loss': 0,
            'push': 0
        }
    }
    for game in res['data']:
        if 'best_bets' not in game:
            continue
        results['num_games'] += 1

        bb = game['best_bets']

        if bb['money_line']['winner'] == 'home':
            if game['team_scoring']['home'][points_key] > game['team_scoring']['away'][points_key]:
                results['money_line']['win'] += 1
            elif game['team_scoring']['home'][points_key] < game['team_scoring']['away'][points_key]:
                results['money_line']['loss'] += 1
            else:
                results['money_line']['push'] += 1
        else:
            if game['team_scoring']['away'][points_key] > game['team_scoring']['home'][points_key]:
                results['money_line']['win'] += 1
            elif game['team_scoring']['away'][points_key] < game['team_scoring']['home'][points_key]:
                results['money_line']['loss'] += 1
            else:
                results['money_line']['push'] += 1

        total = game['team_scoring']['home'][points_key] + \
            game['team_scoring']['away'][points_key]

        if bb['over_under']['winner'] == 'over':
            if total > float(bb['over_under']['points']):
                results['over_under']['win'] += 1
            elif total < float(bb['over_under']['points']):
                results['over_under']['loss'] += 1
            else:
                results['over_under']['push'] += 1
        else:
            if total < float(bb['over_under']['points']):
                results['over_under']['win'] += 1
            elif total > float(bb['over_under']['points']):
                results['over_under']['loss'] += 1
            else:
                results['over_under']['push'] += 1

        home_score = game['team_scoring']['home'][points_key]
        away_score = game['team_scoring']['away'][points_key]

        if bb['spread']['winner'] == 'home':
            home_score += float(bb['spread']['spread'])
        else:
            away_score += float(bb['spread']['spread'])

        if bb['spread']['winner'] == 'home':
            if home_score > away_score:
                results['spread']['win'] += 1
            elif home_score < away_score:
                results['spread']['loss'] += 1
            else:
                results['money_line']['push'] += 1
        else:
            if away_score > home_score:
                results['spread']['win'] += 1
            elif away_score < home_score:
                results['spread']['loss'] += 1
            else:
                results['spread']['push'] += 1

    return results


if __name__ == '__main__':

    for league in LEAGUES:
        d = start_date

        results = {
            'num_games': 0,
            'money_line': {
                'win': 0,
                'loss': 0,
                'push': 0
            },
            'over_under': {
                'win': 0,
                'loss': 0,
                'push': 0
            },
            'spread': {
                'win': 0,
                'loss': 0,
                'push': 0
            }
        }

        while d < datetime.utcnow():
            r = calc_best_bets(d, 'score')

            results['num_games'] += r['num_games']
            for k in ['money_line', 'over_under', 'spread']:
                for kk in ['win', 'loss', 'push']:
                    results[k][kk] += r[k][kk]
            d += timedelta(days=1)
        print(results)
        break
