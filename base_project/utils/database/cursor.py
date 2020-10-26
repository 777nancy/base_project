class CursorFromConnectionFromPool(object):

    def __init__(self, database_connection_pool):
        self._database_connection_pool = database_connection_pool
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """ with ブロックに入る段階で呼び出されます"""
        self.connection = self._database_connection_pool.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ with ブロックから出る段階で呼び出されます"""
        if exc_val is None:
            self.cursor.close()
            self.connection.commit()
        else:
            # トランザクション中にエラー発生。現在のコネクション中に生じた変更を全て取り消します。
            self.connection.rollbak()

        # エラーが発生してもしなくてもコネクションはプールに戻さなければいけません。
        self._database_connection_pool.return_connection(self.connection)
