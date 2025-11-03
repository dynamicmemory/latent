from exchange import Exchange as exchange
from database import Database as database 
from databaseManager import DatabaseManager as databaseManager 
from features import Features as features

base: str = "https://api.bybit.com"
tickers: str = "/v5/market/tickers"
kline: str = "/v5/market/kline"
timeframe: str = "D"
bitcoin: str = "BTCUSDT"


# TODO: Generate name dynamically not hard coded
def main():
    fname: str = f"{bitcoin}-{timeframe}.csv"
    ex = exchange(bitcoin, timeframe)
    db = database(fname)
    dbm = databaseManager(db, ex)
    dbm.update_db()

    f = features(fname)
    f.everything() 

if __name__ == "__main__":
    main()


# Program runs 
# Checks db for history 
# Updates csvs which should be sql dbs 
# Asks what I would like to do? / already knows (design choice here)
  # Auto mode or manual mode maybe....? 
# Calculates features / metrics
# if we are doing NN 
  # Builds NN (NN should already be prebuilt I think)
  # Feeds updated info in and gets answer out 
  # executes on answer 
# if we are doing probabilistic 
  # .... dont know yet

