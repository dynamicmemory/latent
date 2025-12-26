# TODO: Ensure asset name and timeframe are checked for safety b4 db access
from os import utime
from src.agent import Agent
from src.exchange import Exchange
from src.sqlitedb import DatabaseManager
import sys
import time

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "update":
        for tf in ["15", "60", "240", "D", "W"]:
            dbm = DatabaseManager("BTCUSDT", tf) 
            dbm.update_table()
            # print(time.time()*1000)
            # print(dbm.database.get_latest_row()[0])
    else:
        syntra = Agent()
        # dbm = DatabaseManager("BTCUSDT", "15") 
        # dbm.update_table()


if __name__ == "__main__":
    main()
