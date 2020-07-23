import os
import logging
from mongoengine import connect
from pymongo import MongoClient
from fantasystats.tools.singleton import Singleton


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DB_PORT = int(os.environ.get('DB_PORT', 27017))
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', None)
DB_PWD = os.environ.get('DB_PWD', None)
MODE = os.environ.get('MODE', 'local')


class Database(Singleton):

    def __init__(self):

        if MODE == 'local':
            logging.info('In local mode')

            connect('fantasy_data', host=DB_HOST, port=DB_PORT)
            self._db = MongoClient('%s:%s' % (DB_HOST, DB_PORT))[
                'fantasy_data']

        elif MODE in ['prod', 'dev']:
            logging.info('In production mode')

            DB_USER = os.environ.get('DB_USER', None)
            DB_PWD = os.environ.get('DB_PWD', None)

            connect(
                db='fantasy_data',
                ssl=True,
                # ssl_ca_certs='/opt/keys/rds-combined-ca-bundle.pem',
                host=DB_HOST,
                port=DB_PORT,
                username=DB_USER,
                password=DB_PWD
            )

            self._db = MongoClient(
                ssl=True,
                # ssl_ca_certs='/opt/keys/rds-combined-ca-bundle.pem',
                host=DB_HOST,
                port=DB_PORT,
                username=DB_USER,
                password=DB_PWD
            )['fantasy_data']
        else:
            connect('testdb', host='mongomock://localhost')

    def get_database(self):
        return self._db

    @property
    def db(self):
        return self.Instance().get_database()
