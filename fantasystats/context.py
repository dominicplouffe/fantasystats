import os
import redis
import logging
from fantasystats.tools import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_modules = Database.Database()
db = db_modules.get_database()

REDIS = redis.Redis()

API_URL = os.environ.get('API_URL', 'http://localhost:9500/')
