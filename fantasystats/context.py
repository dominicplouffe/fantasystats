import logging
from fantasystats.tools import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_modules = Database.Database()
db = db_modules.get_database()
