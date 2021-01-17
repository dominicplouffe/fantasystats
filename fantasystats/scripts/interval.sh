wget "https://api.connexion.me/api/pongme/start/791901-658653-637354-747231"
PYTHONPATH=/opt/fantasystats python3 /opt/fantasystats/fantasystats/scripts/mlb/interval.py
PYTHONPATH=/opt/fantasystats python3 /opt/fantasystats/fantasystats/scripts/nhl/interval.py
PYTHONPATH=/opt/fantasystats python3 /opt/fantasystats/fantasystats/scripts/nba/interval.py
wget "https://api.connexion.me/api/pongme/end/791901-658653-637354-747231"
