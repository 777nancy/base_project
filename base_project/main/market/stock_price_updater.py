import argparse
import logging
import os
import threading

from base_project import slack
from base_project.main.base import base
from base_project.models.market import stock_price
from base_project.utils import market_data, time_util, util

logger = logging.getLogger(__name__)


class StockPriceUpdater(base.BasicLogic):

    def __init__(self, ticker_symbol, start_date, end_date):

        self._ticker_symbols = ticker_symbol
        self._start_date = start_date
        self._end_date = end_date

        self._slack_notificator = slack.SlackNotificator(util.name2base_name(__name__))
        self._start_time = None

    def run(self):

        threads = []

        for symbol in set(self._ticker_symbols):
            thread = threading.Thread(target=self._update, args=(symbol, ))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def do_after_exception(self, exception):
        self._slack_notificator.notify_from_file(os.path.join('slack', 'utils', 'error.txt'),
                                                 {'traceback': util.exception2str(exception),
                                                  'start_time': self._start_time,
                                                  'end_time': time_util.get_timestamp_now()
                                                  })

    @staticmethod
    def cli(sys_argv):
        parser = argparse.ArgumentParser()

        parser.add_argument('-ts', '--ticker-symbol', nargs='*', required=True)
        parser.add_argument('-st', '--start-date', default=None)
        parser.add_argument('-et', '--end-date', default=None)

        return parser.parse_args(sys_argv)

    def _update(self, symbol):
        start_time = time_util.get_timestamp_now()
        stock_price_obj = stock_price.StockPrice(symbol)
        if stock_price_obj.table_exists():
            if self._start_date:
                latest_date = self._start_date
            else:
                latest_date = stock_price_obj.select_latest_date()
                latest_date = time_util.get_past_date_stamp(latest_date, days=-1)

            market_data_df = market_data.fetch_stock_data_from_yf(symbol, latest_date, self._end_date)
            if len(market_data_df):
                stock_price_obj.insert_market_data_df(market_data_df)
            else:
                logger.info('{} data is up to date'.format(symbol))
        else:
            #  対象データの初回実行時
            stock_price_obj.create_table()
            latest_date = time_util.get_past_date_stamp(years=2)

            try:
                market_data_df = market_data.fetch_stock_data_from_yf(symbol, latest_date, self._end_date)
            except Exception:
                # データ初回投入時のエラー発生後は対象テーブルの削除をおこなう
                stock_price_obj.drop_table()
                raise

            if len(market_data_df):
                try:
                    stock_price_obj.insert_market_data_df(market_data_df)
                except Exception:
                    # データ初回投入時のエラー発生後は対象テーブルの削除をおこなう
                    stock_price_obj.drop_table()
                    raise

            else:
                logger.warning('{} data do not exists'.format(symbol))

        self._slack_notificator.notify_from_file(os.path.join('slack', 'market', 'success.txt'),
                                                 {'ticker_symbol': symbol,
                                                  'start_time': start_time,
                                                  'end_time': time_util.get_timestamp_now()
                                                  })
