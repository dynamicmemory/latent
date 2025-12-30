# Intentionally creating a new connection each time to avoid leaving the db open
# less efficent but we are only making two calls max each usage and only one 
# usage per time frame which could be 15 mins to a week, so managable for now.
# Better solution could be open_connection() and close_connection() functions 
# that the dbm could call, only save one call on the db each time really.
import sqlite3
import re

class Database:
    def __init__(self, db_name:str, table:str) -> None:
        """
        Initializes the database class.

        Args:
            db_name: name of the database being queried.
            table: the name of the table being queried.
        """
        self.db_name: str = db_name
        if not re.fullmatch(r'\w+', table):
             raise ValueError(f"Invalid table name: {table}") 
        self.table_name: str = table


    def create_table(self) -> None:
        """ 
        Creates a table using the table name passed into the database 
        constructor if that table does not exist.
        """

        conn: sqlite3.Connection = sqlite3.connect(f"{self.db_name}")
        with conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    timestamp INTEGER NOT NULL PRIMARY KEY,
                    open NUMERIC NOT NULL,
                    high NUMERIC NOT NULL,
                    low NUMERIC NOT NULL, 
                    close NUMERIC NOT NULL, 
                    volume NUMERIC NOT NULL
                )""")


    def fetch_all_rows(self) -> list:
        """
        Retrieves all rows from the specified table in the database. 

        Returns:
            A list containing all rows from the table or None if the table 
            doesn't exist.
        """
        conn: sqlite3.Connection = sqlite3.connect(f"{self.db_name}")
        with conn:
            return conn.execute(f"""
                       SELECT * FROM {self.table_name} 
                           ORDER BY timestamp ASC""").fetchall()


    def insert_row(self, row) -> None:
        """
        Inserts a single row into the database. 
        """
        conn: sqlite3.Connection = sqlite3.connect(f"{self.db_name}")
        with conn: 
            conn.execute(f"""
                INSERT OR IGNORE INTO {self.table_name}
                (timestamp, open, high, low, close, volume) 
                VALUES (?, ?, ?, ?, ?, ?)""", row)


    def insert_rows(self, rows) -> None:
        """ 
        Inserts all elements from the passed in list 'rows' variable into the 
        database. 
        """
        conn: sqlite3.Connection = sqlite3.connect(f"{self.db_name}")
        with conn:
            conn.executemany(f"""
                INSERT OR IGNORE INTO {self.table_name}
                (timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?)""",rows)


    def get_latest_row(self) -> list:
        """ 
        Gets the last row in the database sorted by the primary key of timestamp 

        Returns:
            row: the last row or most recent row in the database or None if the 
            table doesnt exist.
        """
        conn: sqlite3.Connection = sqlite3.connect(f"{self.db_name}")
        with conn:
            row = conn.execute(f"""
                  SELECT * FROM {self.table_name}
                  ORDER BY timestamp DESC
                  LIMIT 1""").fetchone()
        return row


from src.exchange import Exchange
import pandas as pd
import time

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
        self.db_name = f"{asset}.db"
        self.table_name = f"{self.asset}_{self.timeframe}"
        self.database = Database(self.db_name, self.table_name)
        self.database.create_table() 


    def update_table(self):
        """ 
        Updates the database by n number of rows depending on the time 
        difference between the current unix time vs the last record in the db.
        """
        print(f"Updating table - {self.table_name}")
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

        self.database.insert_rows(rows)
        

    # TODO: It smells, but it works for now, circle back when models built.
    def calculate_missing_rows(self, latest_row: list) -> int: 
        """ 
        Calculates how many rows the database is missing from being up to date.

        Args: 
            latest_row: the last row from the data
        Returns:
            nrows: the number of rows to retrieve from the exchange 
        """
        utc: int = int(time.time()*1000)
        time_map: dict[str, int] = {
                "15": 900000,
                "60": 3600000,
                "240": 14400000,
                "D": 86400000,
                "W": 604800000
        }
        last_timestamp: int = latest_row[0]
        time_step_length: int = time_map[self.timeframe]

        # minus the last timestamp in the database and 1 time step to ensure 
        # we are looking at closed candle time steps only
        adjusted_utc: int = utc - last_timestamp - time_step_length
        nrows: int = int(adjusted_utc / time_step_length)
        print(f"Number of candles to retreive:{nrows}")
        return nrows


    def get_dataframe(self):
        """
        Converts all rows in a database table to a pandas dataframe with the 
        timestamps as the indexes.

        Returns:
            df: a pandas dataframe

        """
        rows: list[tuple] = self.database.fetch_all_rows()
        columns = ["timestamp", "open", "high", "low", "close", "volume"]
        df = pd.DataFrame(rows, columns=columns)
        df.set_index("timestamp", inplace=True)
        
        return df
