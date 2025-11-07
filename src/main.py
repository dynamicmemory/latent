from src.exchange import Exchange as exchange
from src.database import Database as database 
from src.databaseManager import DatabaseManager as databaseManager 
from src.features import Features as features

base: str = "https://api.bybit.com"
tickers: str = "/v5/market/tickers"
kline: str = "/v5/market/kline"
timeframe: str = "D"
bitcoin: str = "BTCUSDT"


# TODO: Generate name dynamically not hard coded
def main():
    #15min
    fname: str = f"{bitcoin}-{"15"}.csv"
    ex = exchange(bitcoin, "15")
    db = database(fname)
    dbm = databaseManager(db, ex)
    dbm.update_db()

    #1hr
    fname: str = f"{bitcoin}-{"60"}.csv"
    ex = exchange(bitcoin, "60")
    db = database(fname)
    dbm = databaseManager(db, ex)
    dbm.update_db()

    #4hr
    fname: str = f"{bitcoin}-{"240"}.csv"
    ex = exchange(bitcoin, "240")
    db = database(fname)
    dbm = databaseManager(db, ex)
    dbm.update_db()


    #weekly
    fname: str = f"{bitcoin}-{"W"}.csv"
    ex = exchange(bitcoin, "W")
    db = database(fname)
    dbm = databaseManager(db, ex)
    dbm.update_db()

    fname: str = f"{bitcoin}-{timeframe}.csv"
    ex = exchange(bitcoin, timeframe)
    db = database(fname)
    dbm = databaseManager(db, ex)
    dbm.update_db()

    f = features(fname)
    f.everything() 

if __name__ == "__main__":
    main()


# Phase 1 
# Run Program
# Checks db for history and syncs up latest price records 
# Calculates features 
# Builds nn
# Comes to a market conclusion

# Phase 2 
# Exchange Auth 
# Manual and auto ability to set and cancel trades 
# Logging of entire system 
# Dashboard viewing integration

# Phase 3 
# End to End mode 
# Rebuild DB in SQLite
# Rebuild agent from NN to probabilistic 

