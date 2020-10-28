import logging
from abc import ABCMeta
from typing import Union

from base_project.utils.database import connection_pool, cursor

logger = logging.getLogger(__name__)


class DatabaseAccess(metaclass=ABCMeta):
    """
    データベースアクセスの行う基底のクラス
    """
    _connection_pool = None

    @staticmethod
    def read_query_from_file(file_path: str, encoding: str = None) -> str:
        """ファイルからクエリを読み込む

        Args:
            file_path: ファイルパス
            encoding: エンコーディング

        Returns:
            ファイルのクエリ文字列
        """
        with open(file_path, mode='r', encoding=encoding) as fin:
            query = fin.read()
        return query

    def execute(self, query: str, params: Union[dict, list, tuple] = None):
        """クエリを実行する

        Args:
            query: クエリ
            params: クエリパラメタ

        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool) as cur:
            cur.execute(query, params)
            logger.info('SQL: {}'.format(cur.query))

    def execute_from_file(self, file_path: str, params: Union[dict, list, tuple] = None, encoding: str = None):
        """ファイルからクエリを読み込み、executeを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            encoding: エンコーディング

        """
        query = self.read_query_from_file(file_path, encoding)
        self.execute(query, params)

    def executemany(self, query: str, params: Union[list, tuple] = None):
        """タプル、リストからデータのINSERTを行う

        Args:
            query: クエリ
            params: インサートのデータ

        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool) as cur:
            cur.executemany(query, params)
            logger.info('SQL: {}'.format(cur.query))

    def executemany_from_file(self, file_path: str, params: Union[dict, list, tuple] = None, encoding: str = None):
        """ファイルからクエリを読み込み、executemanyを実行する

        Args:
            file_path:
            params:
            encoding:

        Returns:

        """
        query = self.read_query_from_file(file_path, encoding)
        self.executemany(query, params)

    def select_all(self, query: str, params: Union[dict, list, tuple] = None) -> tuple:
        """SELECT文を実行し、結果をすべて取得する

        Args:
            query: クエリ
            params: クエリパラメタ

        Returns:
            クエリの実行結果
        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool) as cur:
            cur.execute(query, params)
            logger.info('SQL: {}'.format(cur.query))
            return cur.fetchall()

    def select_all_from_file(self, file_path: str, params: Union[dict, list, tuple] = None,
                             encoding: str = None) -> tuple:
        """ファイルからクエリを読み込み、select_allを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            encoding: エンコーディング

        Returns:
            クエリの実行結果
        """
        query = self.read_query_from_file(file_path, encoding)
        return self.select_all(query, params)

    def select_one(self, query: str, params: Union[dict, list, tuple] = None) -> tuple:
        """SELECT文を実行し、結果の先頭を取得する

        Args:
            query: クエリ
            params: クエリパラメタ

        Returns:
            クエリの実行結果
        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool) as cur:
            cur.execute(query, params)
            logger.info('SQL: {}'.format(cur.query))
            return cur.fetchone()

    def select_one_from_file(self, file_path: str, params: Union[dict, list, tuple] = None,
                             encoding: str = None) -> tuple:
        """ファイルからクエリを読み込み、select_oneを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            encoding: エンコーディング

        Returns:
            クエリの実行結果
        """
        query = self.read_query_from_file(file_path, encoding)
        return self.select_one(query, params)

    def close(self):
        """コネクションをクロースする

        """
        self._connection_pool.close_all_connections()


class PostgreSQLDatabaseAccess(DatabaseAccess):
    """
    PostgreSQLのアクセスを行うクラス
    """

    def __init__(self, minconn: int, maxconn: int, **kwargs: dict):
        """コンストラクタ

        Args:
            minconn: 最小コネクション数
            maxconn: 最大コネクション数
            **kwargs: データベース情報の辞書
        """
        self._connection_pool = connection_pool.PostgreSQLConnectionPool(minconn, maxconn, **kwargs)
