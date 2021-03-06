import os
from abc import ABCMeta
from typing import Union

from base_project import config
from base_project.utils.database import database_accessor

SQl_ROOT_PATH = config.Config.get_instance().SQL_ROOT_PATH


def join_sql_file_path(*sql_file_dirs):
    def _join_sql_file_path(function):
        def __join_sql_file_path(self, file_path, *args, **kwargs):
            abs_sql_file_path = os.path.join(*sql_file_dirs, file_path)
            return function(self, abs_sql_file_path, *args, **kwargs)

        return __join_sql_file_path

    return _join_sql_file_path


class ModelForDatabase(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        self._db = database_accessor.DatabaseAccessorFactory.create(**kwargs)

    def execute(self, query: str, params: Union[dict, list, tuple] = None, raw_params: dict = None):
        """クエリを実行する

        Args:
            query: クエリ
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ

        """
        self._db.execute(query, params, raw_params)

    @join_sql_file_path(SQl_ROOT_PATH)
    def execute_from_file(self, file_path: str, params: Union[dict, list, tuple] = None, raw_params: dict = None,
                          encoding: str = None):
        """ファイルからクエリを読み込み、executeを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ
            encoding: エンコーディング

        """
        self._db.execute_from_file(file_path, params, raw_params, encoding)

    def executemany(self, query: str, params: Union[list, tuple] = None, raw_params: dict = None):
        """タプル、リストからデータのINSERTを行う

        Args:
            query: クエリ
            params: インサートのデータ
            raw_params: formatで設定するパラメタ

        """

        self._db.execute_from_file(query, params, raw_params)

    @join_sql_file_path(SQl_ROOT_PATH)
    def executemany_from_file(self, file_path: str, params: Union[dict, list, tuple] = None, raw_params: dict = None,
                              encoding: str = None):
        """ファイルからクエリを読み込み、executemanyを実行する

        Args:
            file_path: ファイルのパス
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ
            encoding: エンコーディング

        """

        self._db.execute_from_file(file_path, params, raw_params, encoding)

    def select_all(self, query: str, params: Union[dict, list, tuple] = None, raw_params: dict = None) -> tuple:
        """SELECT文を実行し、結果をすべて取得する

        Args:
            query: クエリ
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ

        Returns:
            クエリの実行結果
        """
        return self._db.select_all_from_file(query, params, raw_params)

    @join_sql_file_path(SQl_ROOT_PATH)
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
        return self._db.select_all_from_file(file_path, params, raw_params, encoding)

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
        return self._db.select_many(query, fetch_size, params, raw_params)

    @join_sql_file_path(SQl_ROOT_PATH)
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
        return self._db.select_many_from_file(file_path, fetch_size, params, raw_params, encoding)

    def select_one(self, query: str, params: Union[dict, list, tuple] = None, raw_params: dict = None) -> tuple:
        """SELECT文を実行し、結果の先頭を取得する

        Args:
            query: クエリ
            params: クエリパラメタ
            raw_params: formatで設定するパラメタ

        Returns:
            クエリの実行結果
        """
        return self._db.select_one(query, params, raw_params)

    @join_sql_file_path(SQl_ROOT_PATH)
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
        return self._db.select_one_from_file(file_path, params, raw_params, encoding)

    def read_table_by_name(self, table_name,
                           schema=None,
                           index_col=None,
                           coerce_float=True,
                           parse_dates=None,
                           columns=None,
                           chunksize=None):
        return self._db.read_table_by_name(table_name=table_name,
                                           schema=schema,
                                           index_col=index_col,
                                           coerce_float=coerce_float,
                                           parse_dates=parse_dates,
                                           columns=columns,
                                           chunksize=chunksize)

    def read_table_by_query(self, query,
                            index_col=None,
                            coerce_float=True,
                            params=None,
                            parse_dates=None,
                            chunksize=None):
        return self._db.read_table_by_query(sql=query,
                                            index_col=index_col,
                                            coerce_float=coerce_float,
                                            params=params,
                                            parse_dates=parse_dates,
                                            chunksize=chunksize)

    def write_table(self, dataframe,
                    table_name: str,
                    schema=None,
                    if_exists: str = "fail",
                    index: bool = True,
                    index_label=None,
                    chunksize=None,
                    dtype=None,
                    method=None):
        self._db.write_table(dataframe,
                             table_name=table_name,
                             schema=schema,
                             if_exists=if_exists,
                             index=index,
                             index_label=index_label,
                             chunksize=chunksize,
                             dtype=dtype,
                             method=method
                             )

    def drop_table(self, table_name):
        self._db.drop_table(table_name)

    def table_exists(self, table_name):
        return self._db.table_exists(table_name)

    def close(self):
        """コネクションをクローズする

        """
        self._db.close()
