from abc import ABCMeta, abstractmethod

from psycopg2 import pool


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
