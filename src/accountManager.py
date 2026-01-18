from src.exchange import Exchange

class AccountManager:
    def __init__(self, api_key:str, api_secret:str, testnet:bool=False):
        self.api_key:str = api_key
        self.api_secret:str = api_secret
        self.exchange = Exchange(api_key=self.api_key, 
                                 api_secret=self.api_secret, 
                                 testnet=testnet)

    # Move to account manager.
    def print_all_balances(self) -> None:
        res = self.exchange.get_all_balances()
        if res["retCode"] != 0:
            print(f"Exchange error\ncode: {res["retCode"]}\nmessage: {res["retMsg"]}")
            return -1
        
        coins = res["result"]["list"][0]["coin"]
        total = res["result"]["list"][0]
        print(f"\n{"Coin":<6}{"Amount":>14}{"USD Val":>14}")
        print("-"*34)
        for coin in coins:
            name:str = coin["coin"]
            amount:float = float(coin["walletBalance"])
            usdtot:float = float(coin["usdValue"])
            if name != "USDT":
                print(f"{name:<6}{amount:>14,.4f}{usdtot:>14,.2f}")
            else:
                print(f"{name:<6}{amount:>14,.2f}{usdtot:>14,.2f}")
        print("-"*34)
        print(f"{'Total':<6}{'-':>14}{float(total['totalEquity']):>14,.2f}")


    def get_balance(self, symbol="BTCUSDT") -> float: 
        res = self.exchange.get_balance(symbol)
        if req["retCode"] != 0:
            print(f"Exchange error\ncode: {req["retCode"]}\nmessage: {req["retMsg"]}")
            return -1

        res = req["result"]["list"][0]["coin"][0]["walletBalance"]
        return round(float(res),4)
