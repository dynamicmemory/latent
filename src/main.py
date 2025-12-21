# TODO: Ensure asset name and timeframe are checked for safety b4 db access
from os import utime
from src.agent import Agent
from src.exchange import Exchange
from src.sqlitedb import DatabaseManager

def main():
    # syntra = Agent()
    # syntra.main()
    # e = Exchange("BTCUSDT", "D")
    # print(e.get_ohlc_sql(2))
         
    dbm = DatabaseManager("BTCUSDT", "15")
    dbm.update_rows()
    

    # import time 
    # print(int(time.time()*1000))

if __name__ == "__main__":
    main()
