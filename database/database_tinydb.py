from tinydb import TinyDB, Query

tinydb = TinyDB('tinydb_db.json')

query = Query()

__all__ = ['tinydb', 'query']
