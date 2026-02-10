# TODO: Change how we are pretty printing, perhaps dictionaries or move out of class
# TODO: If an account manager menu class is made, move all pretty printing out 
#       of this class and only returned processed exchange reponses.
from src.exchange.exchange import Exchange
from src.log import Log

class AccountManager:
    def __init__(self, api_key:str, api_secret:str, testnet:bool=False):
        self.api_key:str = api_key
        self.api_secret:str = api_secret
        self.log = Log()
        self.exchange = Exchange(api_key=self.api_key, 
                                 api_secret=self.api_secret, 
                                 testnet=testnet)

    def write_to_log(self, func: str, msg:str, print_msg:bool=False) -> None:
        self.log.write(f"[AccountManager][{func}] - {msg}")
        if print_msg:
            print(msg)


    def check_retcode(self, response:dict) -> int:
        """ Checks the retCode response from a query to the exchange """
        if response["retCode"] != 0:
            c:str = response['retCode']
            m:str = response['retMsg']
            msg:str = f"code: {c} message: {m}"
            self.write_to_log("check_retcode", msg) 

            print("Having trouble contacting exchange, try again shortly.")
            return -1
        else:
            return 0


    def get_balance(self, asset="BTCUSDT") -> float: 
        """ 
        Returns the float value balance of the passed in symbol 

        Args: 
            asset - the asset querying balance for

        Returns:
            res - float value of account balance for the asset of -1 on failure
        """
        res = self.exchange.fetch_balance(asset=asset)
        if self.check_retcode(res) != 0: return -1

        res = res["result"]["list"][0]["coin"][0]["walletBalance"]
        return round(float(res),4)


    def get_position(self, category:str="linear", symbol:str="BTCUSDT") -> tuple:
        res = self.exchange.fetch_position(category, symbol)
        if self.check_retcode(res) != 0: return (-1, "")   # retunr a tuple on failure
        result = res["result"]["list"][0]
        if result["side"] == "Buy":
            return (1, float(result["size"]))
        elif result["side"] == "Sell":
            return (0, result["size"]) 
        else: 
            return (2, "0")


    def create_limit_order(self, asset, side, size, price) -> int:
        """ 
        Sends a limit order to the exchange for execution

        Args: 
            asset - The asset to place an order for, 'BTCUSDT' for example
            side - Buy or Sell
            size - The size of the order in terms of the trading assest
            price - The price to set the order at 

        Returns:
            -1 on failure and 0 on success
        """
        res = self.exchange.send_limit_order("linear", asset, side, size, price)
        if self.check_retcode(res) != 0: 
            return -1

        print("Limit Order Successfully set")
        return 0


    def create_market_order(self, asset, side, size) -> int:
        """
        Sends a market order to the exchange for execution 

        Args: 
            asset - The asset to place an order for, 'BTCUSDT' for example
            side - Buy or Sell
            size - the size of the order in terms of the trading assest

        Returns:
            -1 on failure and 0 on success
        """
        res = self.exchange.send_market_order("linear", asset, side, size)
        if self.check_retcode(res) != 0: 
            return -1

        msg:str = "Market Order Successfully executed"
        self.write_to_log("create_market_order", msg, True)
        return 0
    

    def create_stop_loss(self, asset:str, side:str, size:str, trigger:str, trigger_dir:int) -> int:
        """
        Sends a market order to the exchange for execution 

        Args: 
            asset - The asset to place an order for, 'BTCUSDT' for example
            side - Buy or Sell
            size - the size of the order in terms of the trading assest
            trigger - The price at which to trigger the stop loss 
            trigger_dir - The direction to place the order;
                          1 for rises to, 2 for falls to 

        Returns:
            -1 on failure and 0 on success
        """
        res = self.exchange.set_stop_loss("linear", asset, side, size, trigger, trigger_dir)
        if self.check_retcode(res) != 0: 
            return -1
        msg:str = "Stop loss Successfully set"
        self.write_to_log("create_stop_loss", msg, True)
        return 0
    

    def cancel_order(self, category:str, asset, order_id) -> int:
        """
        Cancels an order that has the passed in order_id

        Args: 
            category - Type of contract 'linear', 'spot', 'options'
            asset - The asset the order is for 
            order_id - The exchange generated id number of the cancelled order
        """
        res = self.exchange.cancel_order(category, order_id["orderId"], asset)
        if self.check_retcode(res) != 0: 
            return -1

        msg:str = "Order successfully Cancelled"
        self.write_to_log("cancel_order", msg, True)
        return 0


    def cancel_all_USDT_orders(self, category:str) -> int:
        res = self.exchange.cancel_all_USDT_orders(category)
        if self.check_retcode(res) != 0: 
            return -1

        msg:str = "All Orders successfully Cancelled"
        self.write_to_log("cancel_all_USDT_orders", msg, True)
        return 0


    def get_last_two_ohlc(self, asset, timeframe) -> tuple:
        res: dict = self.exchange.get_ohlc(asset, timeframe, 2)
        if self.check_retcode(res) != 0: 
            return -1, -1

        return res["result"]["list"][0], res["result"]["list"][1]        

##################### PRETTY PRINTING OF EXCHANGE DATA #########################
    def print_all_balances(self) -> None|int:
        """ Pretty Prints all balances for an account"""
        res = self.exchange.fetch_all_balances()
        if self.check_retcode(res) != 0: return -1
        
        coins = res["result"]["list"][0]["coin"]
        total = res["result"]["list"][0]
        print("*"*75)
        print("BALANCES")
        print(f"\n{"Coin":<6}{"Amount":>14}{"USD Val":>14}")
        print("-"*75)
        for coin in coins:
            name:str = coin["coin"]
            amount:float = float(coin["walletBalance"])
            usdtot:float = float(coin["usdValue"])
            if name != "USDT":
                print(f"{name:<6}{amount:>14,.4f}{usdtot:>14,.2f}")
            else:
                print(f"{name:<6}{amount:>14,.2f}{usdtot:>14,.2f}")
        print("-"*75)
        print(f"{'Total':<6}{'-':>14}{float(total['totalEquity']):>14,.2f}")
        print()


    def print_all_usdt_positions(self) -> None|int:
        """ Pretty Prints all usdt based positions for an account"""
        res = self.exchange.fetch_all_usdt_positions()
        if self.check_retcode(res) != 0: return -1

        positions:list = res["result"]["list"]
        print("*"*75)
        print("\nUSDT POSITIONS")
        print(f"\n{"Market":<9}{"Entry":>10}{"Mark Price":>12}{"Size":>9}{"USD val":>11}{"RPnL":>11}{"UPnL":>11}")
        print("-"*75)
        for position in positions:
            s:str = position["symbol"]
            e:float = float(position["avgPrice"])
            m:str = position["markPrice"]
            q:float = float(position["size"])
            r:float = float(position["curRealisedPnl"])
            u:float = float(position["unrealisedPnl"])
            print(f"{s:<9}{e:>10,.2f}{m:>12}{q:>9}{e*q:>11,.2f}{r:>11,.2f}{u:>11,.2f}")
        print()


    def print_orders(self, category:str, symbol:str) -> list|int:
        """ Pretty Prints all orders for a symbol for an account"""
        res = self.exchange.fetch_orders(category, symbol)
        if self.check_retcode(res) != 0: return -1

        orders:list = res["result"]["list"]
        print("*"*75)
        print("\nORDERS")
        print(f"\n{"No":<4}{"Market":<10}{"Type":<10}{"Direction":<12}{"Price":>12}{"Size":>12}{"USD value":>12}")
        print("-"*75)
        for n, order in enumerate(orders):
            s:str = order["symbol"]
            t:str = order["orderType"]
            d:str = order["side"]
            p:float = float(order["price"])
            q:float = float(order["qty"]) 
            print(f"{n+1:<4}{s:<10}{t:<10}{d:<12}{p:>12,.2f}{q:>12,.4f}{p*q:>12,.2f}")
        return orders
