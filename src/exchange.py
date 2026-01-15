from __future__ import annotations
from sys import exception
from typing import TYPE_CHECKING
import requests as r
import time 
import hashlib
import hmac 
import json 


if TYPE_CHECKING:
    from requests import Response


class Exchange:

    # Dont assign none, have a default symbol, and interval. Figure out the best 
    # way once auth is built out
    def __init__(self, symbol:str|None=None, interval:str|None=None, 
                 api_key:str|None=None, api_secret:str|None=None, 
                 testnet:bool=False):

        self.symbol: str|None = symbol 
        self.interval: str|None = interval
        self.api_key: str|None = api_key
        self.api_secret: str|None = api_secret
        self.base_url: str = self.set_base_url(testnet)

        # Maybe abstract to function 
        self.timestamp: str = str(int(time.time() *1000))
        self.recieve_window: str = str(5000)
        

    def set_base_url(self, testnet:bool) -> str:
        """ Sets the base url for the class

        Args:
            testnet - if True, base url will point to the testnet website, 
                      otherwise the normal exchange will be set
        """
        if testnet:
            return "https://api-testnet.bybit.com"
        else:
            return "https://api.bybit.com"


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


# ----------------------- AUTH RELATED FUNCTIONS & APIS -----------------------
    

    def auth_connection(self):
        """ 
        Called to pass in and api key and secret after an exchange object 
        has already been created, may not be usful to the newer design
        """
        pass 

    def generate_auth_signature(self, params:str) :
        """
        Generates a hash signature of your secret key to send to the exchange

        Args:
            params - the body of your request for the exchange, needed to be 
                     encoded into the hash.
        Returns:
            signature - your secret key and requests hashed for the exchange
        """
        if self.api_secret is None or self.api_key is None: 
            return -1

        m: str = self.timestamp + self.api_key + self.recieve_window + params
        sig = hmac.new(bytes(self.api_secret, "utf-8"), 
                       m.encode("utf-8"),
                       hashlib.sha256).hexdigest()
        return sig


    def make_auth_request(self, params:str):
        """
        May fuse with make_request above, just change to pass in auth treu or false
        """
        if not isinstance(self.generate_auth_signature(params), str):
            #handle no api set 
            pass 

        pass
    
    def get_balance(self):
        pass

    def get_position(self):
        pass 

    def get_orders(self):
        pass 

    def get_last_pnl(self):
        pass 

    def limit_order(self):
        pass 

    def market_order(self):
        pass 

    def cancel_order(self):
        pass 

    def cancel_all_orders(self):
        pass 
