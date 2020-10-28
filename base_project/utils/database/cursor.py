class CursorFromConnectionFromPool(object):
    """
    コネクションプールからカーソルを取得するクラス
    """

    def __init__(self, database_connection_pool):
        """コンストラクタ

        Args:
            database_connection_pool: connection_pool.DatabaseConnectionPoolで定義されたコネクションプール
        """
        self._database_connection_pool = database_connection_pool
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """コネクションプールからコネクション、カーソルを取得する
        
        Returns:
            カーソル
        """
        self.connection = self._database_connection_pool.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """カーソルを閉じ、コネクションをコネクションプールに返却する

        Args:
            exception_type: 例外
            exception_value: エラーメッセージ
            exception_traceback: エラーのトレースバック

        """
        if exception_type is None:
            self.cursor.close()
            self.connection.commit()
        else:
            self.connection.rollbak()

        self._database_connection_pool.return_connection(self.connection)
