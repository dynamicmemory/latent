# TODO: Ensure asset name and timeframe are checked for safety b4 db access
from src.menu import run_main_menu


def main():
    run_main_menu()

    # Temp ability to check db for mistakes
    # from src.sqlitedb import DatabaseManager
    # dbm = DatabaseManager("BTCUSDT", "15")
    # dbm.get_dataframe()

if __name__ == "__main__":
    main()
    



