import logging

from base_project.utils.database import connection_pool
from base_project.utils.database import cursor

logger = logging.getLogger(__name__)


class DatabaseAccess(object):

    def __init__(self, minconn, maxconn, **kwargs):
        self._connection_pool = connection_pool.PgConnectionPool(minconn, maxconn, **kwargs)

    @staticmethod
    def read_query_from_file(file_path, encoding=None):
        with open(file_path, mode='r', encoding=encoding) as fin:
            query = fin.read()
        return query

    def execute(self, query, params=None):
        with cursor.CursorFromConnectionFromPool(self._connection_pool) as cur:
            cur.execute(query, params)
            logger.info('SQL: {}'.format(cur.query))

    def execute_from_file(self, file_path, params=None, encoding=None):
        query = self.read_query_from_file(file_path, encoding)
        return self.execute(query, params)

    def executemany(self, query, params=None):
        with cursor.CursorFromConnectionFromPool(self._connection_pool) as cur:
            cur.executemany(query, params)
            logger.info('SQL: {}'.format(cur.query))

    def executemany_from_file(self, file_path, params=None, encoding=None):
        query = self.read_query_from_file(file_path, encoding)
        return self.executemany(query, params)

    def select_all(self, query, params=None):
        with cursor.CursorFromConnectionFromPool(self._connection_pool) as cur:
            cur.execute(query, params)
            logger.info('SQL: {}'.format(cur.query))
            return cur.fetchall()

    def select_all_from_file(self, file_path, params=None, encoding=None):
        query = self.read_query_from_file(file_path, encoding)
        return self.select_all(query, params)

    def select_one(self, query, params=None):
        with cursor.CursorFromConnectionFromPool(self._connection_pool) as cur:
            cur.execute(query, params)
            logger.info('SQL: {}'.format(cur.query))
            return cur.fetchone()

    def select_one_from_file(self, file_path, params=None, encoding=None):
        query = self.read_query_from_file(file_path, encoding)
        return self.select_one(query, params)
