# TODO: Auth, Personal account ops, fix the ohlc functions since migration
from __future__ import annotations
from sys import exception
from typing import TYPE_CHECKING
import requests as r

if TYPE_CHECKING:
    from requests import Response


class Exchange:

    def __init__(self, symbol: str, interval: str):
        self.symbol: str = symbol 
        self.interval: str = interval
        self.base_url: str = "https://api.bybit.com"


    def make_request(self, method: str, url: str, params: dict) -> dict:
        """ 
        Builds requests to query the exchanges api
        Returns dict - the response as the results or an error code 
        """
        try:
            res: Response = r.request(method, url, params=params)
            return res.json()
        except exception as e:
            print(f"function: make_request in class exchange has failed {e}")
            return None


    def get_ohlc(self, limit=1000) -> list:
        """
        Retrieves the open, high, low and close of the given asset
        """
        kline: str = "/v5/market/kline"
        params: dict = {"category": "linear",
                        "symbol": self.symbol,
                        "interval": self.interval,
                        "limit": limit,
                        }
        json: dict|None = self.make_request("GET", self.base_url+kline, params=params)
        if not json:
            return None

        # self.handle_error(json)

        results = json["result"]["list"]
        results.reverse()
        return results

    def get_closed_candles(self, limit=1000) -> list|None:
        """
        Retrieves the open, high, low and close of close candles only for a 
        given asset.

        Args:
            limit: the number of candles to retrieve from the exchange.
        Returns:
            results: List n candles utcTimestamp + ohlc + volume as int|float.
        """
        # we are removing the last candle which is open, +1 ensures correct number 
        limit = 1000 if limit > 1000 else limit + 1  
        kline: str = "/v5/market/kline"
        params: dict = {"category": "linear",
                        "symbol": self.symbol,
                        "interval": self.interval,
                        "limit": limit,
                        }
        json: dict = self.make_request("GET", self.base_url+kline, params=params)

        if not json:
            return None

        temp = json["result"]["list"]
        temp.reverse()
        results = []
        for line in temp:
            results.append([ int(line[0]), float(line[1]), float(line[2]), 
                             float(line[3]), float(line[4]), float(line[6]) ])

        # Do not return the last candle as it has not closed yet 
        return results[:-1]


    def get_price(self) -> float|None:
        """ 
        Returns the current market price for the symbol provided to the exchange
        """
        ticker: str = "/v5/market/tickers"
        params: dict = {"category": "linear",
                        "symbol": self.symbol,
                        }
        json: dict = self.make_request("GET", self.base_url+ticker, params=params)

        if not json:
            return None

        results: float = float(json["result"]["list"][0]["bid1Price"])
        return results


# ---- TRADE OPERATIONS ----
# ---- ACCOUNT OPERATIONS ----

    # Auth
    # get account details
    # get order details 
    # get position details 
    # make a trade 

