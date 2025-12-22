# TODO: Ensure asset name and timeframe are checked for safety b4 db access
from os import utime
from src.agent import Agent
from src.exchange import Exchange
from src.sqlitedb import DatabaseManager

def main():
    for tf in ["15", "60", "240", "D", "W"]:
        dbm = DatabaseManager("BTCUSDT", tf) 
        dbm.update_table()
    # syntra = Agent()
    # syntra.main()
         


if __name__ == "__main__":
    main()
