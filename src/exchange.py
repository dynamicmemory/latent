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
            signature - your secret key and requests hashed for the exchange on 
                        success and -1 as an int on failure.
        """
        if self.api_secret is None or self.api_key is None: 
            print("Api key or secret has not been set")
            return 0

        # Recalc timestamp so that each request falls within recieve window
        self.timestamp = str(int(time.time() * 1000))

        m: str = self.timestamp + self.api_key + self.recieve_window + params
        sig = hmac.new(bytes(self.api_secret, "utf-8"), 
                       m.encode("utf-8"),
                       hashlib.sha256).hexdigest()
        return sig


    def make_auth_request(self, method:str, url:str, params:str):
        """
        May fuse with make_request above, just change to pass in auth treu or false
        """
        signature: str|int = self.generate_auth_signature(params)
        # print(signature)
        # -1 returned on failure, failure if api key not set.
        if not isinstance(signature, str):
            #handle no api set 
            return 0

        self.timestamp = str(int(time.time() * 1000))

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-SIGN-TYPE": '2',
            "X-BAPI-TIMESTAMP": self.timestamp,
            "X-BAPI-RECV-WINDOW": self.recieve_window,
            "Content-Type": "application/json"
        }

        if method == "GET":
            response = r.get(self.base_url + url + "?" + params, headers=headers).json()
        elif method == "POST":
            response = r.post(self.base_url + url, headers=headers, data=params).json()
        else: 
            response = 0 

        return response


    # May be redundant, unsure on how use will go with all or specific coin only
    def fetch_balance(self, account_type:str="UNIFIED", coin:str="USDT") -> float|int:
        """ Gets the wallet balance of the account """
        params = f"accountType={account_type}&coin={coin}"
        req = self.make_auth_request("GET", "/v5/account/wallet-balance", params) 
        return req


    def fetch_all_balances(self, account_type:str="UNIFIED") -> int|None:
        """ Prints the total account balance as well as each coins total balance"""
        params: str = f"accountType={account_type}"
        req = self.make_auth_request("GET", "/v5/account/wallet-balance", params)
        return req


    def fetch_position(self, category:str="linear", symbol:str="BTCUSDT"):
        params:str=f"category={category}&symbol={symbol}"
        req = self.make_auth_request("GET", "/v5/position/list", params)
        return req


    def fetch_all_positions(self, category:str="linear", settleCoin:str="USDT"):
        params:str=f"category={category}&settleCoin={settleCoin}"
        req = self.make_auth_request("GET", "/v5/position/list", params)
        return req


    def fetch_orders(self, category:str, symbol:str):
        """ Returns all orders for the given symbol on the given contract

        Args:
            category - market type ('linear', 'inverse', 'spot', etc)
            symbol - Trading pair, 'BTCUSDT', etc
        """
        params = f"category={category}&symbol={symbol}&openOnly={0}"
        req = self.make_auth_request("GET", "/v5/order/realtime", params)
        return req


    def fetch_last_pnl(self):
        pass 


    def create_limit_order(self, category:str, symbol:str, side:str, qty:str, price:str):
        """ Sends a limit order to the exchange 

        Args:
            category - market type ('linear', 'inverse', 'spot', etc)
            symbol - Trading pair, 'BTCUSDT', etc
            side - Direction of trade 'Buy' or 'Sell'
            qty - Order quanity in numerator value
            price - Order price
        """
        params = json.dumps({"category":category,
                            "symbol":symbol,
                            "side":side,
                            "orderType":"Limit",
                            "qty":qty,
                            "price":price,
                            "timeInForce":"PostOnly", 
                             })
        req = self.make_auth_request("POST", "/v5/order/create", params)
        return req
         

    # Not tested, test when ready to market buy or sell
    def create_market_order(self, category:str, symbol:str, side:str, qty:str):
        """ Sends a limit order to the exchange 

        Args:
            category - market type ('linear', 'inverse', 'spot', etc)
            symbol - Trading pair, 'BTCUSDT', etc
            side - Direction of trade 'Buy' or 'Sell'
            qty - Order quanity in numerator value
        """
        params = json.dumps({"category":category,
                            "symbol":symbol,
                            "side":side,
                            "orderType":"Market",
                            "qty":qty,
                             })
        req = self.make_auth_request("POST", "/v5/order/create", params)
        return req


    def cancel_order(self, orderId:str):

        pass 

        
    def cancel_all_orders(self, category:str, symbol:str):
        """ Cancels all orders the account has open
        
        Args:
            category - market type ('linear', 'inverse', 'spot', etc)
            symbol - Trading pair, 'BTCUSDT', etc
        """
        params = json.dumps({"category": category,
                             "symbol":symbol,})
        req = self.make_auth_request("POST", "/v5/order/cancel-all", params)
        return req



