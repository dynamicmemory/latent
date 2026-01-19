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


    def print_orders(self, category:str, symbol:str) -> None|int:
        res = self.exchange.fetch_orders(category, symbol)
        if res["retCode"] != 0:
            print(f"Exchange error\ncode: {res["retCode"]}\nmessage: {res["retMsg"]}")
            return -1

        orders:list = res["result"]["list"]
        print("-"*70)
        print("\nORDERS")
        print(f"\n{"Market":<10}{"Type":<10}{"Direction":<12}{"Price":>12}{"Size":>12}{"USD value":>12}")
        print("-"*70)
        for order in orders:
            s:str = order["symbol"]
            t:str = order["orderType"]
            d:str = order["side"]
            p:float = float(order["price"])
            q:float = float(order["qty"]) 
            print(f"{s:<10}{t:<10}{d:<12}{p:>12,.2f}{q:>12,.4f}${p*q:>12,.2f}")


    def print_all_positions(self) -> None|int:
        res = self.exchange.fetch_all_positions()
        if res["retCode"]:
            print(f"Exchange error\ncode: {res["retCode"]}\nmessage: {res["retMsg"]}")
            return -1

        
        positions:list = res["result"]["list"]
        print("-"*70)
        print("\nPOSITIONS")
        print(f"\n{"Market":<12}{"Entry":>10}{"Mark Price":>12}{"Size":>10}{"USD val":>12}{"RPnL":>12}{"UPnL":>12}")
        print("-"*70)
        for position in positions:
            s:str = position["symbol"]
            e:float = float(position["avgPrice"])
            m:str = position["markPrice"]
            q:float = float(position["size"])
            r:float = float(position["curRealisedPnl"])
            u:float = float(position["unrealisedPnl"])
            print(f"{s:<12}{e:>10,.2f}{m:>12}{q:>10}{e*q:>12,.2f}{r:>12,.2f}{u:>12,.2f}")


    def get_balance(self, symbol="BTCUSDT") -> float: 
        res = self.exchange.fetch_balance(symbol)
        if req["retCode"] != 0:
            print(f"Exchange error\ncode: {req["retCode"]}\nmessage: {req["retMsg"]}")
            return -1

        res = req["result"]["list"][0]["coin"][0]["walletBalance"]
        return round(float(res),4)

    
    def cancel_order(self, orderId:str) -> None:
        pass
    
