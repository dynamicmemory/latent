# This class is doing too much and mixing too many concerns, it should be 
# managing responses from the exchange only and either printing or handling 
# the outputs.
from src.exchange import Exchange

class AccountManager:
    def __init__(self, api_key:str, api_secret:str, testnet:bool=False):
        self.api_key:str = api_key
        self.api_secret:str = api_secret
        self.exchange = Exchange(api_key=self.api_key, 
                                 api_secret=self.api_secret, 
                                 testnet=testnet)


    def check_retcode(self, response:dict) -> int:
        if response["retCode"] != 0:
            print(f"Exchange error\ncode: {response["retCode"]}\n\
                    message: {response["retMsg"]}")
            return 0
        else:
            return 1


    def print_all_balances(self) -> None:
        res = self.exchange.fetch_all_balances()
        if res["retCode"] != 0:
            print(f"Exchange error\ncode: {res["retCode"]}\nmessage: {res["retMsg"]}")
            return -1
        
        coins = res["result"]["list"][0]["coin"]
        total = res["result"]["list"][0]
        print("-"*70)
        print("BALANCES")
        print(f"\n{"Coin":<6}{"Amount":>14}{"USD Val":>14}")
        print("-"*70)
        for coin in coins:
            name:str = coin["coin"]
            amount:float = float(coin["walletBalance"])
            usdtot:float = float(coin["usdValue"])
            if name != "USDT":
                print(f"{name:<6}{amount:>14,.4f}{usdtot:>14,.2f}")
            else:
                print(f"{name:<6}{amount:>14,.2f}{usdtot:>14,.2f}")
        print("-"*70)
        print(f"{'Total':<6}{'-':>14}{float(total['totalEquity']):>14,.2f}")


    def print_orders(self, category:str, symbol:str) -> None|int|list:
        res = self.exchange.fetch_orders(category, symbol)
        if res["retCode"] != 0:
            print(f"Exchange error\ncode: {res["retCode"]}\nmessage: {res["retMsg"]}")
            return -1

        orders:list = res["result"]["list"]
        print("-"*70)
        print("\nORDERS")
        print(f"\n{"No":<4}{"Market":<10}{"Type":<10}{"Direction":<12}{"Price":>12}{"Size":>12}{"USD value":>12}")
        print("-"*70)
        for n, order in enumerate(orders):
            s:str = order["symbol"]
            t:str = order["orderType"]
            d:str = order["side"]
            p:float = float(order["price"])
            q:float = float(order["qty"]) 
            print(f"{n+1:<4}{s:<10}{t:<10}{d:<12}{p:>12,.2f}{q:>12,.4f}{p*q:>12,.2f}")
        return orders


    def print_all_usdt_positions(self) -> None|int:
        """ """
        res = self.exchange.fetch_all_usdt_positions()
        if res["retCode"]:
            print(f"Exchange error\ncode: {res["retCode"]}\nmessage: {res["retMsg"]}")
            return -1

        
        positions:list = res["result"]["list"]
        print("-"*70)
        print("\nUSDT POSITIONS")
        print(f"\n{"Market":<9}{"Entry":>10}{"Mark Price":>12}{"Size":>9}{"USD val":>11}{"RPnL":>11}{"UPnL":>11}")
        print("-"*70)
        for position in positions:
            s:str = position["symbol"]
            e:float = float(position["avgPrice"])
            m:str = position["markPrice"]
            q:float = float(position["size"])
            r:float = float(position["curRealisedPnl"])
            u:float = float(position["unrealisedPnl"])
            print(f"{s:<9}{e:>10,.2f}{m:>12}{q:>9}{e*q:>11,.2f}{r:>11,.2f}{u:>11,.2f}")


    def get_balance(self, asset="BTCUSDT") -> float: 
        """ 
        Returns the float value balance of the passed in symbol 

        Args: 
            asset - the asset querying balance for

        Returns:
            res - float value of account balance for the asset of -1 on failure
        """
        res = self.exchange.fetch_balance(asset)
        if req["retCode"] != 0:
            print(f"Exchange error\ncode: {req["retCode"]}\nmessage: {req["retMsg"]}")
            return -1

        res = req["result"]["list"][0]["coin"][0]["walletBalance"]
        return round(float(res),4)


    # This function shouldnt be doing this, it is too much, this class shouldnt 
    # be passing user input, it should only be output info from exchange.
    def create_limit_order(self) -> None:
        """ Asks user for order details and places order with the exchange """
        assets: dict = {1:"BTCUSDT"}
        options:int = len(assets)
        choice:int = 0
        while choice < 1 or choice > options:
            print("Select the asset: ")
            for key in assets.keys():
                print(f"{key}. {assets[key]}")
            try:
                choice = int(input(">> "))
            except TypeError as e: 
                print("Pick a number from the list of options")

        while True:
            print("Select either Buy or Sell\n1. Buy\n2. Sell")
            try:
                side_choice = int(input(">> "))
                if side_choice == 1:
                    side = "Buy"
                    break
                elif side_choice == 2:
                    side = "Sell"
                    break 
                else: 
                    print("Enter either 1 or 2 for your choice")
            except TypeError as e:
                print("Enter either 1 or 2 for your choice")

        print("Enter the price: ")
        price = input(">> ")

        print("Enter the amount: ")
        size = input(">> ")

        res = self.exchange.send_limit_order("linear", assets[choice], side, size, price)
        if res["retCode"] == 0:
            print("Order Successfully set")
        else:
            print(f"Exchange error\ncode: {req["retCode"]}\nmessage: {req["retMsg"]}")


    # Copy paste of limit order and should not go here.
    def create_market_order(self) -> None:
        assets: dict = {1:"BTCUSDT"}
        options:int = len(assets)
        choice:int = 0
        while choice < 1 or choice > options:
            print("Select the asset for market order: ")
            for key in assets.keys():
                print(f"{key}. {assets[key]}")
            try:
                choice = int(input(">> "))
            except TypeError as e: 
                print("Pick a number from the list of options")

        while True:
            print("Select either Buy or Sell\n1. Buy\n2. Sell")
            try:
                side_choice = int(input(">> "))
                if side_choice == 1:
                    side = "Buy"
                    break
                elif side_choice == 2:
                    side = "Sell"
                    break 
                else: 
                    print("Enter either 1 or 2 for your choice")
            except TypeError as e:
                print("Enter either 1 or 2 for your choice")

        print("Enter the amount: ")
        size = input(">> ")

        res = self.exchange.send_market_order("linear", assets[choice], side, size)
        if res["retCode"] == 0:
            print("Order Successfully set")
        else:
            print(f"Exchange error\ncode: {res["retCode"]}\nmessage: {res["retMsg"]}")
    
    # This is written so poorly as well
    def cancel_order(self, category:str="linear") -> None:

        assets: dict = {1:"BTCUSDT"}
        options:int = len(assets)
        choice:int = 0
        while choice < 1 or choice > options:
            print("Select the asset: ")
            for key in assets.keys():
                print(f"{key}. {assets[key]}")
            try:
                choice = int(input(">> "))
            except TypeError as e: 
                print("Pick a number from the list of options")
        orders:list = self.print_orders(category, assets[choice])

        n = 0
        if len(orders) == 0:
            print("There are no orders to cancel")
            return -1

        while True:
            print("Select the 'No' of the order you want to cancel")
            try:
                n = int(input(">> "))
                if n > 0 and n <= len(orders):
                    break
            except TypeError as e:
                print("Enter a number only")

        res = self.exchange.cancel_order(category, orders[n-1]["orderId"], assets[choice])
        if res["retCode"] == 0:
            print("Successfully cancelled order")
        else:
            print(f"Exchange error\ncode: {res["retCode"]}\nmessage: {res["retMsg"]}")
