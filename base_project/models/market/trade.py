import dataclasses
from dataclasses import dataclass


@dataclass
class Deal:
    ticker_symbol: str
    buying_price: float
    selling_price: float = dataclasses.field(default=None, init=False)


@dataclass
class Stock:
    ticker_symbol: str


class Dealer(object):

    def __init__(self):
        self._dealing_dict = {}
        self._dealt_dict = {}

    def buy(self, ticker_symbol, buying_price):

        deals = self._dealing_dict.get(ticker_symbol)

        if deals:
            deals.append(Deal(ticker_symbol=ticker_symbol, buying_price=buying_price))
        else:
            self._dealing_dict[ticker_symbol] = [Deal(ticker_symbol=ticker_symbol, buying_price=buying_price)]

    def sell(self, ticker_symbol, selling_price):

        deals = self._dealing_dict.get(ticker_symbol)

        for deal in deals:
            deal.selling_price = selling_price

        dealt = self._dealt_dict.get(ticker_symbol)

        if dealt:
            dealt.extend(deals)
        else:
            self._dealt_dict[ticker_symbol] = []
            for deal in deals:
                self._dealt_dict[ticker_symbol].append(deal)

        self._dealing_dict[ticker_symbol] = []

    def calculate_profit(self):
        profit = 0.0
        for ticker_symbol, deals in self._dealt_dict.items():
            for deal in deals:
                profit += deal.selling_price - deal.buying_price
        return profit


if __name__ == '__main__':
    d = Dealer()

    d.buy('amzn', 100)
    d.buy('amzn', 50)
    d.sell('amzn', 25)
    d.buy('amzn', 50)
    print(d.calculate_profit())
