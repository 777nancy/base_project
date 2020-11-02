# Standard Library
import logging
from abc import ABCMeta, abstractmethod
from typing import Union

from base_project.utils.database import connection_pool, cursor

logger = logging.getLogger(__name__)


class DatabaseAccess(metaclass=ABCMeta):
    """
    データベースアクセスの行う基底のクラス
    """
    _connection_pool = None
    _dict_cursor = False

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

    @staticmethod
    def _execute(cur, query, params=None, raw_params=None):
        if raw_params:
            query = query.format(**raw_params)

        cur.execute(query, params)
        logger.info('SQL: {}'.format(cur.query.decode()))
        return cur

    def execute(self, query: str, params: Union[dict, list, tuple] = None, raw_params: dict = None):
        """クエリを実行する

        Args:
            query: クエリ
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ
            
        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool, self._dict_cursor) as cur:
            self._execute(cur, query, params, raw_params)

    def execute_from_file(self, file_path: str, params: Union[dict, list, tuple] = None, raw_params: dict = None,
                          encoding: str = None):
        """ファイルからクエリを読み込み、executeを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ
            encoding: エンコーディング
            
        """
        query = self.read_query_from_file(file_path, encoding)
        self.execute(query, params, raw_params)

    def executemany(self, query: str, params: Union[list, tuple] = None, raw_params: dict = None):
        """タプル、リストからデータのINSERTを行う

        Args:
            query: クエリ
            params: インサートのデータ
            raw_params: formatで設定するパラメタ

        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool, self._dict_cursor) as cur:
            if raw_params:
                query = query.format(**raw_params)

            cur.executemany(query, params)
            logger.info('SQL: {}'.format(cur.query.decode()))

    def executemany_from_file(self, file_path: str, params: Union[dict, list, tuple] = None, raw_params: dict = None,
                              encoding: str = None):
        """ファイルからクエリを読み込み、executemanyを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ
            encoding: エンコーディング

        """
        query = self.read_query_from_file(file_path, encoding)
        self.executemany(query, params, raw_params)

    def select_all(self, query: str, params: Union[dict, list, tuple] = None, raw_params: dict = None) -> tuple:
        """SELECT文を実行し、結果をすべて取得する

        Args:
            query: クエリ
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ

        Returns:
            クエリの実行結果
        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool, self._dict_cursor) as cur:
            self._execute(cur, query, params, raw_params)
            return cur.fetchall()

    def select_all_from_file(self, file_path: str, params: Union[dict, list, tuple] = None, raw_params: dict = None,
                             encoding: str = None) -> tuple:
        """ファイルからクエリを読み込み、select_allを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ
            encoding: エンコーディング

        Returns:
            クエリの実行結果
        """
        query = self.read_query_from_file(file_path, encoding)
        return self.select_all(query, params, raw_params)

    def select_many(self, query: str, fetch_size: int, params: Union[dict, list, tuple] = None,
                    raw_params: dict = None) -> tuple:
        """SELECT文を実行し、結果をすべて取得する

        Args:
            query: クエリ
            fetch_size: 取得行の数
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ

        Returns:
            クエリの実行結果
        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool, self._dict_cursor) as cur:
            self._execute(cur, query, params, raw_params)
            return cur.fetchmany(fetch_size)

    def select_many_from_file(self, file_path: str, fetch_size: int, params: Union[dict, list, tuple] = None,
                              raw_params: dict = None,
                              encoding: str = None) -> tuple:
        """ファイルからクエリを読み込み、select_allを実行する

        Args:
            file_path: ファイルのパス
            fetch_size: 取得行の数
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ
            encoding: エンコーディング

        Returns:
            クエリの実行結果
        """
        query = self.read_query_from_file(file_path, encoding)
        return self.select_many(query, fetch_size, params, raw_params)

    def select_one(self, query: str, params: Union[dict, list, tuple] = None, raw_params: dict = None) -> tuple:
        """SELECT文を実行し、結果の先頭を取得する

        Args:
            query: クエリ
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ

        Returns:
            クエリの実行結果
        """
        with cursor.CursorFromConnectionFromPool(self._connection_pool, self._dict_cursor) as cur:
            self._execute(cur, query, params, raw_params)
            return cur.fetchone()

    def select_one_from_file(self, file_path: str, params: Union[dict, list, tuple] = None, raw_params: dict = None,
                             encoding: str = None) -> tuple:
        """ファイルからクエリを読み込み、select_oneを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ
            encoding: エンコーディング

        Returns:
            クエリの実行結果
        """
        query = self.read_query_from_file(file_path, encoding)
        return self.select_one(query, params, raw_params)

    @abstractmethod
    def drop_table(self, table_name):

        raise NotImplementedError

    @abstractmethod
    def table_exists(self, table_name):
        raise NotImplementedError

    def close(self):
        """コネクションをクロースする

        """
        self._connection_pool.close_all_connections()


class PostgreSQLAccess(DatabaseAccess):
    """
    PostgreSQLのアクセスを行うクラス
    """

    def __init__(self, minconn: int, maxconn: int, dict_cursor=False, **kwargs: dict):
        """コンストラクタ

        Args:
            minconn: 最小コネクション数
            maxconn: 最大コネクション数
            **kwargs: データベース情報の辞書
        """
        self._connection_pool = connection_pool.PostgreSQLConnectionPool(minconn, maxconn, **kwargs)
        self._dict_cursor = dict_cursor

    def drop_table(self, table_names):

        if type(table_names) is str:
            table_names = [table_names]

        for table_name in table_names:
            self.execute('DROP TABLE IF EXISTS {table_name}', raw_params={'table_name': table_name})

    def table_exists(self, table_name):

        row = self.select_one('SELECT * FROM information_schema.tables WHERE table_name = %(table_name)s',
                              params={'table_name': table_name})

        if row:
            return True
        else:
            return False


class DatabaseAccessFactory(object):

    @classmethod
    def create(cls, **kwargs):
        rdbms = kwargs.get('rdbms').lower()
        kwargs.pop('rdbms')
        if rdbms == 'postgresql':
            return PostgreSQLAccess(**kwargs)
        elif rdbms is None:
            raise KeyError('rdbms is not set')
        else:
            raise ValueError('{} of Access class not exists'.format(rdbms))
