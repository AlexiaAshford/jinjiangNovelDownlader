from tinydb import TinyDB, Query
import logging


tinydb = TinyDB('log_db.json')

query = Query()

__all__ = ['tinydb', 'query']
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)