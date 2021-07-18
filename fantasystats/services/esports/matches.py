from fantasystats.managers.esports import matches
from fantasystats.services import search


def get_match(game_id):
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
    other_bets = {}

    for b in match.bets:
        if b['Name'] == 'Winner':
            for t in b['Odds']:
                team_name = search.get_esport_team_key(t['Name'])
                winner_bet[team_name] = {
                    'name': t['Name'],
                    'odds': float(t['Value']),
                    'team_key': team_name
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

        print(b['Name'])
        print(b['Odds'])
        print('')

    match_info['odds'] = {
        'moneyline': winner_bet,
        'spread': handicap_bet,
        'other': other_bets,
    }

    return match_info
