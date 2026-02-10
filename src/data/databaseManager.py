from src.exchange.exchange import Exchange
from src.data.database import Database
from src.log import Log
import pandas as pd
import time
import csv

UTC: int = int(time.time()*1000)
TIME_MAP: dict[str, int] = {
    "15": 900000,
    "60": 3600000,
    "240": 14400000,
    "D": 86400000,
    "W": 604800000
}

class DatabaseManager:
    def __init__(self, asset:str, timeframe:str) -> None:
        """
        Initializes the databaseManagement system for controlling the flow of 
        data to and from the database. 

        Args:
            asset: the asset being stored and queried.
            timeframe: the timeframe being looked at for storage and queried.
        """
        self.asset = asset 
        self.timeframe = timeframe
        self.db_name = f"./data/{asset}.db"
        self.table_name = f"{self.asset}_{self.timeframe}"
        self.database = Database(self.db_name, self.table_name)
        self.database.create_table() 
        self.log = Log()


    def update_table(self):
        """ 
        Updates the database by n number of rows depending on the time 
        difference between the current unix time vs the last record in the db.
        """
        self.database.open()
        msg:str = f"Updating table - {self.table_name}"
        self.log.write(f"[DatabaseManager][update_table] - {msg}")
        e = Exchange(self.asset, self.timeframe)

        # Check for an empty table before querying latest row, add as test 
        latest_row = self.database.get_latest_row()
        if latest_row is None:
            print(f"Table-{self.table_name} is empty, fetching max candles")
            rows = e.get_closed_candles()
        else: 
            nrows = self.calculate_missing_rows(latest_row)
            if not nrows: return                       # Exit if no rows needed

            rows = e.get_closed_candles(nrows)
            if rows is None:
                print("Exchange returned None for get_closed_candles, try again soon")
                return 

        self.database.insert_rows(rows)
        self.database.close()
        

    # TODO: It smells, but it works for now, circle back when models built.
    def calculate_missing_rows(self, latest_row: list) -> int: 
        """ 
        Calculates how many rows the database is missing from being up to date.

        Args: 
            latest_row: the last row from the data
        Returns:
            nrows: the number of rows to retrieve from the exchange 
        """
        last_timestamp: int = latest_row[0]
        time_step_length: int = TIME_MAP[self.timeframe]

        # minus the last timestamp in the database and 1 time step to ensure 
        # we are looking at closed candle time steps only
        adjusted_utc: int = UTC - last_timestamp - time_step_length
        nrows: int = int(adjusted_utc / time_step_length)

        msg:str = f"Number of candles to retreive:{nrows}"
        self.log.write(f"[DatabaseManager][calculate_missing_rows] - {msg}")

        return nrows


    def get_dataframe(self, show:bool=False):
        """
        Converts all rows in a database table to a pandas dataframe with the 
        timestamps as the indexes.

        Returns:
            df: a pandas dataframe

        """
        self.database.open()
        rows: list[tuple] = self.database.fetch_all_rows()

        # Print the df is asked too
        if show:
            for row in rows:
                print(row)

        self.database.close()
        columns = ["timestamp", "open", "high", "low", "close", "volume"]
        df = pd.DataFrame(rows, columns=columns)
        df.set_index("timestamp", inplace=True)
        
        return df


    def export_csv(self) -> None:
        """Exports the contents of the current table to a csv file"""
        self.database.open()
        rows: list = self.database.fetch_all_rows()
        columns: list = ["timestamp","open","high","low","close","volume"]

        with open(f"./data/{self.table_name}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

        self.database.close()
        msg:str = f"Successfully exported {self.table_name} table to csv"
        self.log.write(f"[DatabaseManager][export_csv] - {msg}")

