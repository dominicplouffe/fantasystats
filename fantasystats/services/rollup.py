import pytz
from fantasystats.services.nhl import game as nhl_svc
from fantasystats.services.nba import game as nba_svc
from fantasystats.services.mlb import game as mlb_svc
from fantasystats.managers.nhl.odds_rollup import insert_rollup as nhl_mgr
from fantasystats.managers.nba.odds_rollup import insert_rollup as nba_mgr
from fantasystats.managers.mlb.odds_rollup import insert_rollup as mlb_mgr
from datetime import datetime, timedelta
from fantasystats.services.rollup_diff import NBA_DIFF


def rollup_team_odds_results(season, to_date, svc, mgr, pts_key):

    teams = svc.get_all_teams(season)
    odds_rollup = {}
    points = {}
    trends = {}

    for team in teams:
        print('*'*25)
        print(team['team_id'])
        print('*'*25)

        if team['abbr'] == 'DRT':
            continue

        # for g in svc.get_game_by_team(season, team['team_id']):
        #     print(g['game_status'], g['game_date'], g['game_type'])
        games = [
            g for g in svc.get_game_by_team(season, team['team_id'])
            if g['game_status'] in ['Final', 'F'] and g['game_type'] in [
                '2', 'R'
            ]
        ]

        print(len(games))

        result = {
            'noline': {
                'overall': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'otl': 0,
                    'per': 0.00,
                    'pos': 0
                },
                'home': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'otl': 0,
                    'per': 0.00,
                    'pos': 0
                },
                'away': {
                    'games': 0,
                    'wins': 0,
                    'otl': 0,
                    'losses': 0,
                    'per': 0.00,
                    'pos': 0
                }
            },
            'spread': {
                'overall': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'per': 0.00,
                    'pos': 0,
                    'push': 0
                },
                'home': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'per': 0.00,
                    'pos': 0,
                    'push': 0
                },
                'away': {
                    'games': 0,
                    'wins': 0,
                    'losses': 0,
                    'per': 0.00,
                    'pos': 0,
                    'push': 0
                }
            },
            'over_under': {
                'overall': {
                    'games': 0,
                    'over': 0,
                    'under': 0,
                    'push': 0,
                    'per': 0.00,
                    'pos': 0
                },
                'home': {
                    'games': 0,
                    'over': 0,
                    'under': 0,
                    'push': 0,
                    'per': 0.00,
                    'pos': 0
                },
                'away': {
                    'games': 0,
                    'over': 0,
                    'under': 0,
                    'push': 0,
                    'per': 0.00,
                    'pos': 0
                }
            },
            'points': {
                'overall': {
                    'for': 0,
                    'aga': 0
                },
                'home': {
                    'for': 0,
                    'aga': 0
                },
                'away': {
                    'for': 0,
                    'aga': 0
                }
            }
        }

        if team['team_id'] not in points:
            points[team['team_id']] = {
                'overall': {
                    'for': 0,
                    'aga': 0
                },
                'home': {
                    'for': 0,
                    'aga': 0
                },
                'away': {
                    'for': 0,
                    'aga': 0
                }
            }

        if team['team_id'] not in trends:
            trends[team['team_id']] = []

        for g in games:
            if team['team_id'] == g['home_team']['team_id']:
                points[team['team_id']
                       ]['overall']['for'] += g['team_scoring']['home'][pts_key]
                points[team['team_id']
                       ]['overall']['aga'] += g['team_scoring']['away'][pts_key]

                points[team['team_id']
                       ]['home']['for'] += g['team_scoring']['home'][pts_key]
                points[team['team_id']
                       ]['home']['aga'] += g['team_scoring']['away'][pts_key]
            else:
                points[team['team_id']
                       ]['overall']['for'] += g['team_scoring']['away'][pts_key]
                points[team['team_id']
                       ]['overall']['aga'] += g['team_scoring']['home'][pts_key]

                points[team['team_id']
                       ]['away']['for'] += g['team_scoring']['away'][pts_key]
                points[team['team_id']
                       ]['away']['aga'] += g['team_scoring']['home'][pts_key]

            if 'odds' not in g:
                continue
            if 'consensus' not in g['odds']:
                continue

            if g['game_date'] > to_date:
                continue

            home_score = g['team_scoring']['home'][pts_key] + \
                float(g['odds']['consensus']['spread']['home']['spread'])
            away_score = g['team_scoring']['away'][pts_key]

            total = g['team_scoring']['home'][pts_key] + \
                g['team_scoring']['away'][pts_key]
            ou_score = float(
                g['odds']['consensus']['over_under']['over']['points']
            )

            result['points']['overall']['for'] = points[team['team_id']
                                                        ]['overall']['for']
            result['points']['overall']['aga'] = points[team['team_id']
                                                        ]['overall']['aga']

            result['points']['home']['for'] = points[team['team_id']
                                                     ]['home']['for']
            result['points']['home']['aga'] = points[team['team_id']
                                                     ]['home']['aga']

            result['points']['away']['for'] = points[team['team_id']
                                                     ]['away']['for']
            result['points']['away']['aga'] = points[team['team_id']
                                                     ]['away']['aga']

            result['noline']['overall']['games'] += 1
            result['spread']['overall']['games'] += 1
            result['over_under']['overall']['games'] += 1

            trend_game = {
                'overall': {
                    'result': None,
                    'home_score': g['team_scoring']['home'][pts_key],
                    'away_score': g['team_scoring']['away'][pts_key]
                },
                'spread': {
                    'result': None,
                    'spread': g['odds']['consensus']['spread']['home']['spread']
                },
                'over_under': {
                    'result': None,
                    'score': total,
                    'over_under': ou_score
                },
                'side': 'home',
                'home_team': g['home_team']['abbr'],
                'away_team': g['away_team']['abbr'],
                'game_key': g['game_key'],
                'game_date': g['game_date']
            }

            if total > ou_score:
                result['over_under']['overall']['over'] += 1
                trend_game['over_under']['result'] = 'over'
            elif total < ou_score:
                result['over_under']['overall']['under'] += 1
                trend_game['over_under']['result'] = 'under'
            else:
                result['over_under']['overall']['push'] += 1
                trend_game['over_under']['result'] = 'push'

            if team['team_id'] == g['home_team']['team_id']:
                result['noline']['home']['games'] += 1
                result['spread']['home']['games'] += 1
                result['over_under']['home']['games'] += 1

                if home_score > away_score:
                    result['spread']['overall']['wins'] += 1
                    result['spread']['home']['wins'] += 1
                    trend_game['spread']['result'] = 'win'
                elif away_score == home_score:
                    result['spread']['overall']['push'] += 1
                    result['spread']['home']['push'] += 1
                    trend_game['spread']['result'] = 'push'
                else:
                    result['spread']['overall']['losses'] += 1
                    result['spread']['home']['losses'] += 1
                    trend_game['spread']['result'] = 'loss'

                if total > ou_score:
                    result['over_under']['home']['over'] += 1
                elif total < ou_score:
                    result['over_under']['home']['under'] += 1
                else:
                    result['over_under']['home']['push'] += 1

                if g['team_scoring']['home'][pts_key] > g['team_scoring']['away'][pts_key]:
                    result['noline']['overall']['wins'] += 1
                    result['noline']['home']['wins'] += 1
                    trend_game['overall']['result'] = 'win'
                else:
                    if pts_key in ['score', 'runs']:
                        result['noline']['overall']['losses'] += 1
                        result['noline']['home']['losses'] += 1
                    else:
                        loss_key = 'losses'
                        if g['current_period'] >= 4:
                            loss_key = 'otl'
                        result['noline']['overall'][loss_key] += 1
                        result['noline']['home'][loss_key] += 1
                    trend_game['overall']['result'] = 'loss'

            else:
                trend_game['side'] = 'away'
                trend_game['spread']['spread'] = g['odds']['consensus']['spread']['away']['spread']

                result['noline']['away']['games'] += 1
                result['spread']['away']['games'] += 1
                result['over_under']['away']['games'] += 1

                if away_score > home_score:
                    result['spread']['overall']['wins'] += 1
                    result['spread']['away']['wins'] += 1
                    trend_game['spread']['result'] = 'win'
                elif away_score == home_score:
                    result['spread']['overall']['push'] += 1
                    result['spread']['away']['push'] += 1
                    trend_game['spread']['result'] = 'push'
                else:
                    result['spread']['overall']['losses'] += 1
                    result['spread']['away']['losses'] += 1
                    trend_game['spread']['result'] = 'loss'

                if total > ou_score:
                    result['over_under']['away']['over'] += 1
                elif total < ou_score:
                    result['over_under']['away']['under'] += 1
                else:
                    result['over_under']['away']['push'] += 1

                if g['team_scoring']['away'][pts_key] > g['team_scoring']['home'][pts_key]:
                    result['noline']['overall']['wins'] += 1
                    result['noline']['away']['wins'] += 1
                    trend_game['overall']['result'] = 'win'
                else:
                    if pts_key in ['score', 'runs']:
                        result['noline']['overall']['losses'] += 1
                        result['noline']['away']['losses'] += 1
                    else:
                        loss_key = 'losses'
                        if g['current_period'] >= 4:
                            loss_key = 'otl'
                        result['noline']['overall'][loss_key] += 1
                        result['noline']['away'][loss_key] += 1
                    trend_game['overall']['result'] = 'loss'
            trends[team['team_id']].append(trend_game)

        if pts_key in ['score'] and to_date >= datetime(2021, 2, 23):
            result['spread']['overall']['wins'] += NBA_DIFF[team['abbr']
                                                            ]['spread']['overall']['wins']
            result['spread']['overall']['losses'] += NBA_DIFF[team['abbr']
                                                              ]['spread']['overall']['losses']
            result['spread']['overall']['push'] += NBA_DIFF[team['abbr']
                                                            ]['spread']['overall']['push']
            result['spread']['home']['wins'] += NBA_DIFF[team['abbr']
                                                         ]['spread']['home']['wins']
            result['spread']['home']['losses'] += NBA_DIFF[team['abbr']
                                                           ]['spread']['home']['losses']
            result['spread']['home']['push'] += NBA_DIFF[team['abbr']
                                                         ]['spread']['home']['push']
            result['spread']['away']['wins'] += NBA_DIFF[team['abbr']
                                                         ]['spread']['away']['wins']
            result['spread']['away']['losses'] += NBA_DIFF[team['abbr']
                                                           ]['spread']['away']['losses']
            result['spread']['away']['push'] += NBA_DIFF[team['abbr']
                                                         ]['spread']['away']['push']

            result['over_under']['overall']['over'] += NBA_DIFF[team['abbr']
                                                                ]['over_under']['overall']['over']
            result['over_under']['overall']['under'] += NBA_DIFF[team['abbr']
                                                                 ]['over_under']['overall']['under']
            result['over_under']['overall']['push'] += NBA_DIFF[team['abbr']
                                                                ]['over_under']['overall']['push']
            result['over_under']['home']['over'] += NBA_DIFF[team['abbr']
                                                             ]['over_under']['home']['over']
            result['over_under']['home']['under'] += NBA_DIFF[team['abbr']
                                                              ]['over_under']['home']['under']
            result['over_under']['home']['push'] += NBA_DIFF[team['abbr']
                                                             ]['over_under']['home']['push']
            result['over_under']['away']['over'] += NBA_DIFF[team['abbr']
                                                             ]['over_under']['away']['over']
            result['over_under']['away']['under'] += NBA_DIFF[team['abbr']
                                                              ]['over_under']['away']['under']
            result['over_under']['away']['push'] += NBA_DIFF[team['abbr']
                                                             ]['over_under']['away']['push']

        odds_rollup[team['team_id']] = result

    odds_rollup = odds_rollup.items()
    for o in odds_rollup:
        for key in ['spread', 'noline']:
            if o[1][key]['overall']['games'] > 0:
                o[1][key]['overall']['per'] = o[1][key][
                    'overall']['wins'] / o[1][key]['overall']['games']

            if o[1][key]['home']['games'] > 0:
                o[1][key]['home']['per'] = o[1][key][
                    'home']['wins'] / o[1][key]['home']['games']

            if o[1][key]['away']['games'] > 0:
                o[1][key]['away']['per'] = o[1][key][
                    'away']['wins'] / o[1][key]['away']['games']

        if o[1]['over_under']['overall']['games'] > 0:
            o[1]['over_under']['overall']['per'] = o[1]['over_under'][
                'overall']['over'] / o[1]['over_under']['overall']['games']

        if o[1]['over_under']['home']['games'] > 0:
            o[1]['over_under']['home']['per'] = o[1]['over_under'][
                'home']['over'] / o[1]['over_under']['home']['games']

        if o[1]['over_under']['away']['games'] > 0:
            o[1]['over_under']['away']['per'] = o[1]['over_under'][
                'away']['over'] / o[1]['over_under']['away']['games']

    for pkey in ['noline', 'spread', 'over_under']:
        for key in ['overall', 'home', 'away']:
            odds_rollup = sorted(
                odds_rollup,
                key=lambda x: - x[1][pkey][key]['per']
            )

            for i, o in enumerate(odds_rollup):
                o[1][pkey][key]['pos'] = i + 1

    for key in ['overall', 'home', 'away']:
        odds_rollup = sorted(
            odds_rollup,
            key=lambda x: - x[1]['points'][key]['for']
        )

        for i, o in enumerate(odds_rollup):
            o[1]['points'][key]['for-pos'] = i + 1

        odds_rollup = sorted(
            odds_rollup,
            key=lambda x: x[1]['points'][key]['aga']
        )

        for i, o in enumerate(odds_rollup):
            o[1]['points'][key]['aga-pos'] = i + 1

    for o in odds_rollup:
        rec = o[1]
        tre = trends[o[0]]

        if len(tre) > 5:
            tre = tre[-5:]

        mgr(
            rec['noline'],
            rec['spread'],
            rec['over_under'],
            rec['points'],
            o[0],
            to_date,
            tre
        )


if __name__ == '__main__':
    date = datetime.now(pytz.UTC)
    today = datetime(date.year, date.month, date.day)

    date = today - timedelta(days=1)

    # for i in range(0, 3):
    rollup_team_odds_results('20202021', date, nhl_svc, nhl_mgr, 'goals')
    rollup_team_odds_results('2020-2021', date, nba_svc, nba_mgr, 'score')
    rollup_team_odds_results('2021', date, mlb_svc, mlb_mgr, 'runs')
    date += timedelta(days=1)
