from collections import defaultdict


def get_odds_consensus(odds):

    odds_con_stats = {
        'money_line': {
            'away': {'odds': defaultdict(int)},
            'home': {'odds': defaultdict(int)}
        },
        'spread': {
            'away': {'odds': defaultdict(int), 'spread': defaultdict(int)},
            'home': {'odds': defaultdict(int), 'spread': defaultdict(int)},
        },
        'over_under': {
            'over': {'points': defaultdict(int), 'odds': defaultdict(int)},
            'under': {'points': defaultdict(int), 'odds': defaultdict(int)},
        }
    }

    for k, v in odds.items():
        ml = v['money_line']
        sp = v['spread']
        ou = v['over_under']

        for kk, vv in ml.items():
            odds_con_stats['money_line'][kk]['odds'][vv['odds']] += 1

        for kk, vv in sp.items():
            odds_con_stats['spread'][kk]['odds'][vv['odds']] += 1
            odds_con_stats['spread'][kk]['spread'][vv['spread']] += 1

        for kk, vv in ou.items():
            odds_con_stats['over_under'][kk]['odds'][vv['odds']] += 1
            odds_con_stats['over_under'][kk]['points'][vv['points']] += 1

    if len(odds_con_stats['money_line']['away']['odds']) == 0:
        return {
            'money_line': {
                'away': {'odds': "0"},
                'home': {'odds': "0"}
            },
            'spread': {
                'away': {'odds': "0", 'spread': "0"},
                'home': {'odds': "0", 'spread': "0"},
            },
            'over_under': {
                'over': {'points': "0", 'odds': "0"},
                'under': {'points': "0", 'odds': "0"},
            }
        }

    return {
        'money_line': {
            'away': {
                'odds': sorted(
                    odds_con_stats['money_line']['away']['odds'].items(),
                    key=lambda x: - x[1]
                )[0][0]
            },
            'home': {
                'odds': sorted(
                    odds_con_stats['money_line']['home']['odds'].items(),
                    key=lambda x: - x[1]
                )[0][0]
            }
        },
        'spread': {
            'away': {
                'odds': sorted(
                    odds_con_stats['spread']['away']['odds'].items(),
                    key=lambda x: - x[1]
                )[0][0],
                'spread': sorted(
                    odds_con_stats['spread']['away']['spread'].items(),
                    key=lambda x: - x[1]
                )[0][0]
            },
            'home': {
                'odds':  sorted(
                    odds_con_stats['spread']['home']['odds'].items(),
                    key=lambda x: - x[1]
                )[0][0],
                'spread': sorted(
                    odds_con_stats['spread']['home']['spread'].items(),
                    key=lambda x: - x[1]
                )[0][0]
            },
        },
        'over_under': {
            'over': {
                'points': sorted(
                    odds_con_stats['over_under']['over']['points'].items(),
                    key=lambda x: - x[1]
                )[0][0],
                'odds': sorted(
                    odds_con_stats['over_under']['over']['odds'].items(),
                    key=lambda x: - x[1]
                )[0][0],
            },
            'under': {
                'points': sorted(
                    odds_con_stats['over_under']['under']['points'].items(),
                    key=lambda x: - x[1]
                )[0][0],
                'odds': sorted(
                    odds_con_stats['over_under']['under']['odds'].items(),
                    key=lambda x: - x[1]
                )[0][0],
            },
        }
    }


def get_prediction_consensus(predictions):

    pred_con = defaultdict(int)

    for p in predictions:

        if p.payload['away']['score'] > p.payload['home']['score']:
            pred_con['away'] += 1
        else:
            pred_con['home'] += 1

    return pred_con
