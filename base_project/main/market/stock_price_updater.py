import argparse
import contextlib
import os
import logging

from base_project import slack
from base_project.main.base import base
from base_project.models.market import stock_price
from base_project.utils import market_data, time_util, util

logger = logging.getLogger(__name__)


class StockPriceUpdater(base.BasicLogic):

    def __init__(self, ticker_symbol, start_date, end_date):
        super().__init__()

        self._ticker_symbols = ticker_symbol
        self._start_date = start_date
        self._end_date = end_date

        self._slack_notificator = slack.SlackNotificator(__name__)
        self._start_time = None

    def run(self):
        for symbol in self._ticker_symbols:
            self._start_time = time_util.get_timestamp_now()
            stock_price_obj = stock_price.StockPrice(symbol)
            with contextlib.ExitStack() as stack:
                stack.callback(stock_price_obj.close)
                if stock_price_obj.table_exists():
                    if self._start_date:
                        latest_date = self._start_date
                    else:
                        latest_date = stock_price_obj.select_latest_date()
                        latest_date = time_util.get_past_date_stamp(latest_date, days=-1)
                else:
                    stock_price_obj.create_table()
                    latest_date = time_util.get_past_date_stamp(years=2)

                market_data_df = market_data.fetch_stock_data_from_yf(symbol, latest_date, self._end_date)
                if len(market_data_df):
                    stock_price_obj.insert_market_data_df(market_data_df)
            self._slack_notificator.notify_from_file(os.path.join('slack', 'market', 'success.txt'),
                                                     {'ticker_symbol': symbol,
                                                      'start_time': self._start_time,
                                                      'end_time': time_util.get_timestamp_now()
                                                      })

    def do_after_exception(self, exception):
        self._slack_notificator.notify_from_file(os.path.join('slack', 'utils', 'error.txt'),
                                                 {'traceback': util.exception2str(exception),
                                                  'start_time': self._start_time,
                                                  'end_time': time_util.get_timestamp_now()
                                                  })

    @staticmethod
    def cli(sys_argv):
        parser = argparse.ArgumentParser()

        parser.add_argument('-ts', '--ticker-symbol', nargs='*')
        parser.add_argument('-st', '--start-date', default=None)
        parser.add_argument('-et', '--end-date', default=None)

        return parser.parse_args(sys_argv)
