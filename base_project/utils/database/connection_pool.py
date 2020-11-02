from abc import ABCMeta, abstractmethod

import sqlalchemy
from psycopg2 import pool
from sqlalchemy import pool


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

    def __init__(self, url, max_overflow, pool_size):
        self._engine = sqlalchemy.create_engine(url, pool_size=int(pool_size), max_overflow=int(max_overflow),
                                                poolclass=pool.QueuePool)

    def get_connection(self):
        return self._engine.raw_connection()

    def return_connection(self, connection):
        connection.close()

    def close_all_connections(self):
        self._engine.dispose()
