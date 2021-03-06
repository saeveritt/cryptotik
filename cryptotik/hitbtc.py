import requests
from .common import APIError, headers

class Hitbtc:

    url = 'http://api.hitbtc.com/api/1/public/'
    delimiter = ""
    headers = headers

    @classmethod
    def format_pair(cls, pair):
        """format the pair argument to format understood by remote API."""
        pair = pair.replace("-", cls.delimiter).upper()
        return pair

    @classmethod
    def api(cls, url):
        '''call api'''

        try:
            result = requests.get(url, headers=cls.headers, timeout=3)
            assert result.status_code == 200
            return result.json()
        except requests.exceptions.RequestException as e:
            raise APIError(e)

    @classmethod
    def get_market_ticker(cls, pair):
        '''returns simple current market status report'''

        return cls.api(cls.url + cls.format_pair(pair) + "/ticker")

    @classmethod
    def get_market_trade_history(cls, pair):
        '''get market trade history'''

        return cls.api(cls.url + cls.format_pair(pair) \
        + "/trades/recent?max_results=1000&format_item=object")

    @classmethod
    def get_market_order_book(cls, pair):
        '''return order book for the market'''

        return cls.api(cls.url + cls.format_pair(pair) \
        + "/orderbook?format_price=number&format_amount=number")

    @classmethod
    def get_market_spread(cls, pair):
        '''return first buy order and first sell order'''

        from decimal import Decimal

        order_book = cls.get_market_order_book(pair)

        ask = order_book["asks"][0][0]
        bid = order_book["bids"][0][0]

        return Decimal(ask) - Decimal(bid)

    @classmethod
    def get_market_depth(cls, pair):
        '''return sum of all bids and asks'''

        from decimal import Decimal

        order_book = cls.get_market_order_book(pair)
        asks = sum([Decimal(i[1]) for i in order_book["asks"]])
        bid = sum([Decimal(i[0]) * Decimal(i[1]) for i in order_book["bids"]])

        return {"bids": bid, "asks": asks}

