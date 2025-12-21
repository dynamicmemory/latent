import sqlite3
import os as os 
from src.exchange import Exchange


class Database:
    def __init__(self, db_name:str, table:str) -> None:
        """
        Initializes the database class.

        Args:
            db_name: name of the database being queried.
            table: the name of the table being queried.
        """
        self.conn: sqlite3.Connection = sqlite3.connect(f"{db_name}.db")
        self.table_name = table


    def create_table(self) -> None:
        """ 
        Creates a table using the table name passed into the database 
        constructor if that table does not exist.
        """
        with self.conn:
            self.conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    timestamp INTEGER NOT NULL PRIMARY KEY,
                    open NUMERIC NOT NULL,
                    high NUMERIC NOT NULL,
                    low NUMERIC NOT NULL, 
                    close NUMERIC NOT NULL, 
                    volume NUMERIC NOT NULL
                )"""
            )


    def read(self):
        pass 


    def insert(self):
        pass 


    def delete(self):
        pass


    def insert_rows(self, rows):
        with self.conn:
            self.conn.executemany(f"""
                INSERT OR IGNORE INTO {self.table_name}
                (timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?)""",rows)


    def get_latest_row(self):
        with self.conn:
            row = self.conn.execute(f"""
                  SELECT * FROM {self.table_name}
                  ORDER BY timestamp DESC
                  LIMIT 1""").fetchone()
        return row


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


    def update_rows(self):
        """ 
        Updates the database by n number of rows depending on the time 
        difference between the current unix time vs the last record in the db.
        """
        e = Exchange(self.asset, self.timeframe)

        # Possibly move to time utils for other classes to use later on
        # Move this to time util class or clac exhcange
        import time 
        utc: int = int(time.time()*1000)
        time_map: dict[str, int] = {
                "15": 900000,
                "60": 3600000,
                "240": 14400000,
                "D": 86400000,
                "W": 604800000
        }


        # Check for an empty table before querying latest row, add as test 
        latest_row = self.database.get_latest_row()
        if latest_row is None:
            # Normally just fetch max rows 1000 if now rows 
            print(f"Table {self.table_name} is empty, fetching row from exchange")
            # but for current testing just get three so we can display and see
            latest_row = e.get_ohlc_sql(3)
            print(f"Exchange last rows: ")
            for r in latest_row:
                print(r)
            # Set theorectical last row of db to 3rd row back in time from exchange
            latest_row = latest_row[0]

        print(f"Latest row: {latest_row}")
        last_timestamp = latest_row[0]
        print(f"Last timestamp: {last_timestamp}")

        time_step_length: int = time_map[self.timeframe]
        number_of_rows: int = int((utc - last_timestamp) / time_step_length) + 1
        print(f"Number of rows:{number_of_rows}")
        temprows = e.get_ohlc_sql(number_of_rows)
        rows = []

        for r in temprows:
            if r[0] + time_map[self.timeframe] > utc:
                continue 
            rows.append(r)

        # self.database.insert_rows(rows)
        print(rows)

        






