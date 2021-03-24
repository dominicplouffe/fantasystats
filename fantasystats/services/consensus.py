from collections import defaultdict, OrderedDict
import copy


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

    if 'FanDuel' not in odds:
        return None
    order = OrderedDict()
    order['Unibet'] = odds.get('Unibet', odds['FanDuel'])
    order['BetMGM'] = odds.get('BetMGM', odds['FanDuel'])  # TODO - Fix
    order['Sugarhouse'] = odds.get('Sugarhouse', odds['FanDuel'])
    order['FanDuel'] = odds['FanDuel']
    order['PointsBet'] = odds.get('PointsBet', odds['FanDuel'])
    order['DraftKings'] = odds.get('DraftKings', odds['FanDuel'])

    order['Unibet']['link'] = 'https://affiliates.bettingnews.com/register/ubet/'
    order['BetMGM']['link'] = 'https://affiliates.bettingnews.com/register/bmgm/'
    order['Sugarhouse']['link'] = 'https://affiliates.bettingnews.com/register/sugho/'
    order['FanDuel']['link'] = 'https://affiliates.bettingnews.com/register/fd/'
    order['PointsBet']['link'] = 'https://affiliates.bettingnews.com/register/pb/'
    order['DraftKings']['link'] = 'https://affiliates.bettingnews.com/register/dk/'

    return order


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

    data = {
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

    return data


def get_prediction_consensus(predictions, odd_consensus):

    # odd_consensus = copy.deepcopy(odd_consensus)
    pred_con = defaultdict(int)
    picks = {}

    for p in predictions:
        over_under = None
        spread = None
        money_line = None

        if p.payload['away']['score'] > p.payload['home']['score']:
            pred_con['away'] += 1
        else:
            pred_con['home'] += 1

        if 'money_line' in odd_consensus:
            home_payload = float(p.payload['home']['score'])
            away_payload = float(p.payload['away']['score'])
            total = home_payload + away_payload

            try:
                ou_points = float(
                    odd_consensus['over_under']['over']['points']
                )
                if total > ou_points:
                    over_under = odd_consensus['over_under']['over']
                    over_under['pick'] = 'over'
                else:
                    over_under = odd_consensus['over_under']['under']
                    over_under['pick'] = 'under'
            except ValueError:
                over_under = None

            home_spread = float(odd_consensus['spread']['home']['spread'])
            away_spread = float(odd_consensus['spread']['away']['spread'])

            if away_payload > home_payload:
                money_line = odd_consensus['money_line']['away']
                money_line['pick'] = 'away'
            else:
                money_line = odd_consensus['money_line']['home']
                money_line['pick'] = 'home'

            if home_spread > 0:
                home_payload += home_spread
                if home_payload >= away_payload:
                    spread = odd_consensus['spread']['home']
                    spread['pick'] = 'home'
                else:
                    spread = odd_consensus['spread']['away']
                    spread['pick'] = 'away'
            else:
                away_payload += away_spread
                if away_payload >= home_payload:
                    spread = odd_consensus['spread']['away']
                    spread['pick'] = 'away'
                else:
                    spread = odd_consensus['spread']['home']
                    spread['pick'] = 'home'

            picks[p.provider] = {
                'over_under': over_under,
                'spread': spread,
                'money_line': money_line
            }

    return {
        'predictions': pred_con,
        'picks': picks
    }


def get_best_bets(pred_sites, odds_sites):

    over_under_cnt = defaultdict(int)
    over_under_choice = 'over'

    spread_cnt = defaultdict(int)
    spread_choice = 'home'

    money_line_cnt = defaultdict(int)
    money_line_choice = 'home'

    for site in pred_sites:
        over_under_cnt[site['picks']['over_under']['pick']] += 1
        spread_cnt[site['picks']['spread']['pick']] += 1
        money_line_cnt[site['picks']['money_line']['pick']] += 1

    if over_under_cnt.get('under', 0) > over_under_cnt.get('over', 0):
        over_under_choice = 'under'

    if spread_cnt.get('away', 0) > spread_cnt.get('home', 0):
        spread_choice = 'away'

    if money_line_cnt.get('away', 0) > money_line_cnt.get('home', 0):
        money_line_choice = 'away'

    best_bets = {
        'money_line': {
            'odds': None,
            'winner': money_line_choice,
            'site': None,
            'link': None
        },
        'spread': {
            'odds': None,
            'spread': None,
            'winner': spread_choice,
            'site': None,
            'link': None
        },
        'over_under': {
            'odds': None,
            'points': None,
            'winner': over_under_choice,
            'site': None,
            'link': None
        }
    }

    for site, odds in odds_sites.items():

        if 'money_line' not in odds:
            continue

        money_line = odds['money_line'][money_line_choice]
        over_under = odds['over_under'][over_under_choice]
        spread = odds['spread'][spread_choice]

        if money_line['odds'] != 'n/a':
            if best_bets['money_line']['odds'] is None:
                best_bets['money_line']['odds'] = money_line['odds']
                best_bets['money_line']['site'] = site
                best_bets['money_line']['link'] = odds['link']
            elif float(money_line['odds']) > float(
                best_bets['money_line']['odds']
            ):
                best_bets['money_line']['odds'] = money_line['odds']
                best_bets['money_line']['site'] = site
                best_bets['money_line']['link'] = odds['link']

        if spread['odds'] != 'n/a' and float(spread['spread']) != 0.0:
            if best_bets['spread']['odds'] is None:
                best_bets['spread']['odds'] = spread['odds']
                best_bets['spread']['spread'] = spread['spread']
                best_bets['spread']['site'] = site
                best_bets['spread']['link'] = odds['link']
            elif float(spread['odds']) > float(
                best_bets['spread']['odds']
            ):
                best_bets['spread']['odds'] = spread['odds']
                best_bets['spread']['spread'] = spread['spread']
                best_bets['spread']['site'] = site
                best_bets['spread']['link'] = odds['link']

        if over_under['odds'] != 'n/a' and float(over_under['points']) > 0:
            if best_bets['over_under']['odds'] is None:
                best_bets['over_under']['odds'] = over_under['odds']
                best_bets['over_under']['points'] = over_under['points']
                best_bets['over_under']['site'] = site
                best_bets['over_under']['link'] = odds['link']
            elif float(over_under['odds']) > float(
                best_bets['over_under']['odds']
            ):
                best_bets['over_under']['odds'] = over_under['odds']
                best_bets['over_under']['points'] = over_under['points']
                best_bets['over_under']['site'] = site
                best_bets['over_under']['link'] = odds['link']

    return best_bets
