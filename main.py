from exchange import Exchange as exchange
from database import Database as database 
from databaseManager import DatabaseManager as databaseManager 

base: str = "https://api.bybit.com"
tickers: str = "/v5/market/tickers"
kline: str = "/v5/market/kline"
timeframe: str = "D"
bitcoin: str = "BTCUSDT"


# TODO: Generate name dynamically not hard coded
def main():
    ex = exchange(bitcoin, timeframe)
    db = database(f"{bitcoin}-{timeframe}.csv")
    dbm = databaseManager(db, ex)
    dbm.update_db()


if __name__ == "__main__":
    main()

