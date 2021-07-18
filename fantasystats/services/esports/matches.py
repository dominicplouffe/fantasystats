from fantasystats.managers.esports import matches
from fantasystats.services import search


def get_matches_by_date(game_date, category=None, event_id=None):

    all_matches = []

    for m in matches.get_matches_by_date(game_date):

        if category:
            if m.category != category:
                continue

        if event_id:
            if m.event_id != event_id:
                continue

        all_matches.append(get_match(m['game_key'], match=m))

    return all_matches


def get_match(game_id, match=None):
    if not match:
        match = matches.get_match_by_game_key(game_id)

    if not match:
        return {}

    match_info = {
        'game_date': match.game_date,
        'start_time': match.start_time,
        'match_name': match.match_name,
        'match_id': match.match_id,
        'event_name': match.event_name,
        'event_id': match.event_id,
        'category': match.category,
        'competitors': match.competitors,
        'score': match.score.split(':')
    }

    match_info['game_date'] = match_info['game_date'].strftime('%Y-%m-%d')
    match_info['start_time'] = match_info['start_time'].strftime(
        '%Y-%m-%d %H:%M'
    )

    winner_bet = {}
    handicap_bet = {}
    over_under = {}
    other_bets = {}

    for b in match.bets:
        if b['Name'] in ['Winner', '1x2']:
            for t in b['Odds']:
                team_name = search.get_esport_team_key(t['Name'])
                winner_bet[team_name] = {
                    'name': t['Name'],
                    'odds': float(t['Value']),
                    'team_key': team_name
                }
        elif b['Name'] == 'Total':
            for t in b['Odds']:
                if t['Name'].startswith('over'):
                    over_under['over'] = {
                        'spread': t['Name'].split(' ')[-1],
                        'odds': float(t['Value'])
                    }
                else:
                    over_under['under'] = {
                        'spread': t['Name'].split(' ')[-1],
                        'odds': float(t['Value'])
                    }

        elif b['Name'].lower().endswith('handicap'):
            for t in b['Odds']:
                name = t['Name'].split('(')[0].strip()
                team_name = search.get_esport_team_key(name)
                handicap_bet[team_name] = {
                    'name': name,
                    'odds': float(t['Value']),
                    'team_key': team_name,
                    'spread': t['Name'].split('(')[1][:-1]
                }
        else:
            odds = {}
            for t in b['Odds']:
                name = t['Name']
                spread = None
                if '(' in name:
                    name = t['Name'].split('(')[0].strip()
                    spread = t['Name'].split('(')[1][:-1]
                team_name = search.get_esport_team_key(name)
                odds[team_name] = {
                    'name': name,
                    'odds': float(t['Value']),
                    'team_key': team_name,
                }
                if spread:
                    odds[team_name]['spread'] = spread
            b['bet_name'] = b['Name']
            other_bets[b['Name']] = odds

    match_info['odds'] = {
        'moneyline': winner_bet,
        'spread': handicap_bet,
        'total': over_under,
        'other': other_bets,
    }

    return match_info
