import os

import sqlalchemy

from base_project import config
from base_project.models.base import base


class StockPrice(base.ModelForDatabase):

    def __init__(self, table_name):
        self._table_name = table_name
        self._config = config.Config.get_instance()
        super(StockPrice, self).__init__(**self._config.MARKET_DB)

    def create_table(self):
        sql_file_path = os.path.join('market', 'create_table.sql')
        self.execute_from_file(sql_file_path, raw_params={'table_name': self._table_name})

    def insert_market_data_df(self, market_data_df):
        engine = sqlalchemy.create_engine(self._config.MARKET_DB_URL)
        market_data_df.index.name = 'date'
        market_data_df.columns = ['high', 'low', 'open', 'close', 'volume', 'adj_close']
        market_data_df.to_sql(self._table_name, engine, if_exists='append')

    def select_latest_date(self):
        sql_file_path = os.path.join('market', 'select_latest_date.sql')
        latest_date = self.select_one_from_file(sql_file_path, raw_params={'table_name': self._table_name})[0]
        return latest_date

    def drop_table(self, **kwargs):
        super().drop_table(self._table_name)

    def table_exists(self, **kwargs):
        return super().table_exists(self._table_name)

if __name__ == '__main__':
    s = StockPrice('qqq')
    s.drop_table()