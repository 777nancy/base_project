import logging
from abc import ABCMeta, abstractmethod

import sqlalchemy
from psycopg2 import pool
from sqlalchemy import pool

logger = logging.getLogger(__name__)


class DatabaseConnectionPool(metaclass=ABCMeta):
    """
    データベースのコネクションを管理するクラスのインターフェース
    """

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def return_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def close_all_connections(self):
        pass


class PostgreSQLConnectionPool(DatabaseConnectionPool):
    """
    PostgreSQLのコネクションプールを管理するクラス
    """

    def __init__(self, minconn, maxconn, **kwargs):
        """コンストラクタ

        Args:
            minconn: 最小コネクション数
            maxconn: 最大コネクション数
            **kwargs: データベース情報の辞書
        """
        self._connection_pool = pool.SimpleConnectionPool(minconn=minconn, maxconn=maxconn, **kwargs)

    def get_connection(self):
        """コネクションプールからコネクションを取得する

        Returns:
            コネクション
        """
        return self._connection_pool.getconn()

    def return_connection(self, connection):
        """コネクションプールへコネクションを返却する

        Args:
            connection: コネクション

        """
        self._connection_pool.putconn(connection)

    def close_all_connections(self):
        """コネクションプールのコネクションをすべてクローズする
        """
        self._connection_pool.closeall()


class SqlAlchemyConnectionPool(DatabaseConnectionPool):
    """
    sqlalchemyを利用したコネクションプール管理クラス
    """

    @property
    def engine(self):
        return self._engine

    def __init__(self, url, max_overflow, pool_size):
        self._engine = sqlalchemy.create_engine(url, pool_size=int(pool_size), max_overflow=int(max_overflow),
                                                poolclass=pool.QueuePool)

    def get_connection(self):
        return self._engine.raw_connection()

    def return_connection(self, connection):
        connection.close()

    def close_all_connections(self):
        self._engine.dispose()


class ConnectionPoolManager(object):
    connection_pool_dict = {}

    @classmethod
    def get_or_create_connection_pool(cls, url, max_overflow, pool_size):
        connection_pool = cls.connection_pool_dict.get(url)

        if connection_pool:
            logger.debug('got connection pool: {}'.format(url))
            return connection_pool
        else:
            connection_pool = SqlAlchemyConnectionPool(url=url,
                                                       max_overflow=max_overflow,
                                                       pool_size=pool_size)

            cls.connection_pool_dict[url] = connection_pool

            logger.debug('created connection pool: {}'.format(url))

            return connection_pool

    @classmethod
    def close_connection_pools(cls):
        if cls.connection_pool_dict:
            for k, v in cls.connection_pool_dict.items():
                v.close_all_connections()
                logger.debug('closed connection pool: {}'.format(k))

    @classmethod
    def close_connection_pool(cls, connection_pool):

        connection_pool.close_all_connections()

        for k, v in cls.connection_pool_dict.items():

            if v is connection_pool:
                cls.connection_pool_dict.pop(k)

                logger.debug('closed connection pool: {}'.format(k))
                break
