from collections import defaultdict


def find_best_odds(odds):

    best = {
        'money_line': {
            'away': {'odds': None},
            'home': {'odds': None}
        },
        'spread': {
            'away': {'spread': None, 'odds': None},
            'home': {'spread': None, 'odds': None},
        },
        'over_under': {
            'over': {'points': None, 'odds': None},
            'under': {'points': None, 'odds': None},
        }
    }

    for k, v in odds.items():
        if 'money_line' not in v:
            continue

        # SPREAD
        for side in ['home', 'away']:
            try:
                value = float(v['spread'][side]['spread'])
                odds_value = float(v['spread'][side]['odds'])

                if best['spread'][side]['spread'] is None:
                    best['spread'][side]['spread'] = value
                    best['spread'][side]['odds'] = odds_value

                elif value > best['spread'][side]['spread']:
                    best['spread'][side]['spread'] = value
                    best['spread'][side]['odds'] = odds_value
                elif value == best['spread'][side]['spread']:
                    if odds_value > best['spread'][side]['odds']:
                        best['spread'][side]['odds'] = odds_value
            except ValueError:
                pass

        # MONEY LINE
        for side in ['home', 'away']:
            try:
                value = float(v['money_line'][side]['odds'])
                if best['money_line'][side]['odds'] is None:
                    best['money_line'][side]['odds'] = value
                elif value > best['money_line'][side]['odds']:
                    best['money_line'][side]['odds'] = value
            except ValueError:
                pass

        # OVER/UNDER
        for side in ['over', 'under']:

            try:
                value = float(v['over_under'][side]['points'])
                odds_value = float(v['over_under'][side]['odds'])
                if value == 0:
                    continue
                if best['over_under'][side]['points'] is None:
                    best['over_under'][side]['points'] = value
                    best['over_under'][side]['odds'] = odds_value

                elif side == 'over':
                    if value < best['over_under'][side]['points']:
                        best['over_under'][side]['points'] = value
                        best['over_under'][side]['odds'] = odds_value
                    elif value == best['over_under'][side]['points']:
                        if odds_value > best['over_under'][side]['odds']:
                            best['over_under'][side]['odds'] = odds_value
                else:
                    if value > best['over_under'][side]['points']:
                        best['over_under'][side]['points'] = value
                        best['over_under'][side]['odds'] = odds_value
                    elif value == best['over_under'][side]['points']:
                        if odds_value > best['over_under'][side]['odds']:
                            best['over_under'][side]['odds'] = odds_value

            except ValueError:
                pass

    # Now that we know the best, mark the odds that are the best with a flag
    for k, v in odds.items():
        if 'money_line' not in v:
            continue

        # SPREAD
        for side in ['home', 'away']:
            value = float(v['spread'][side]['spread'])
            odds_value = float(v['spread'][side]['odds'])

            if value == best['spread'][side]['spread']:
                if odds_value == best['spread'][side]['odds']:
                    v['spread'][side]['best'] = True
                else:
                    v['spread'][side]['best'] = False
            else:
                v['spread'][side]['best'] = False

        # MONEY LINE
        for side in ['home', 'away']:
            try:
                value = float(v['money_line'][side]['odds'])
                if value == best['money_line'][side]['odds']:
                    v['money_line'][side]['best'] = True
                else:
                    v['money_line'][side]['best'] = False

            except ValueError:
                pass

        # OVER/UNDER
        for side in ['over', 'under']:
            value = float(v['over_under'][side]['points'])
            odds_value = float(v['over_under'][side]['odds'])

            if value == best['over_under'][side]['points']:
                if odds_value == best['over_under'][side]['odds']:
                    v['over_under'][side]['best'] = True
                else:
                    v['over_under'][side]['best'] = False
            else:
                v['over_under'][side]['best'] = False

    return odds


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
        if 'money_line' not in v:
            continue
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
