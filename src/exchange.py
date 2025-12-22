# TODO: Auth, Personal account ops
from __future__ import annotations
from typing import TYPE_CHECKING

import requests as r
from src.database import Database 

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
        res: Response = r.request(method, url, params=params)
        code: int = res.status_code
        if code == 200:
            return res.json()
        else:
            return {"code": code}

    # TODO: Needs type conversion before returning, NOT TO BE DONE TILL DB MIGRATION
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
        json: dict = self.make_request("GET", self.base_url+kline, params=params)

        self.handle_error(json)

        results = json["result"]["list"]
        results.reverse()
        return results


    # Temp for sql testing
    def get_closed_candles(self, limit=1000) -> list:
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

        self.handle_error(json)

        temp = json["result"]["list"]
        temp.reverse()
        results = []
        for line in temp:
            results.append(
                [int(line[0]), 
                 float(line[1]), 
                 float(line[2]),
                 float(line[3]),
                 float(line[4]),
                 float(line[6])])
        return results[:-1]


    def get_price(self) -> dict:
        """ 
        Returns the current market price for the symbol provided to the exchange
        """
        ticker: str = "/v5/market/tickers"
        params: dict = {"category": "linear",
                        "symbol": self.symbol,
                        }
        json: dict = self.make_request("GET", self.base_url+ticker, params=params)

        self.handle_error(json)
        results = json["result"]["list"][0]["bid1Price"]
        print(results)
        return results


    # TODO: Fully explore the full range of errors and come up with robust system
    def handle_error(self, json: dict):
        """
        Takes care of any responses that return error codes
        Returns: Unsure yet 
        """
        # TODO: Handle the non 200 error return correctly, currently returning None
        if json.get("code") != 200:
            return None

        # Check to make sure the request worked
        if json.get("retCode") != 0:
            print(f"ERROR - retCode: {json['retCode']} - {json['retMsg']}")
            code, msg = json.get("retCode"), json.get("retMsg")
            raise Exception(f"ERROR - retCode: {code} - {msg}")

        return None


# ---- TRADE OPERATIONS ----
# ---- ACCOUNT OPERATIONS ----

    # Auth
    # get account details
    # get order details 
    # get position details 
    # make a trade 

