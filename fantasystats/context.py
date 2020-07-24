import logging
from fantasystats.tools import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_modules = Database.Database()
db = db_modules.get_database()

API_URL = 'http://localhost:9500/'

MLB_GAME_API = 'https://statsapi.mlb.com/api/v1.1/game/%s/feed/live'
