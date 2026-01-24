""" Database class for the trading system. Only key point to remember when 
interfacing with the database, is you must call open first before any other 
operations on the database, and call closed once you are finish.
"""
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
        self.conn: sqlite3.Connection = sqlite3.connect(self.db_name)

        if not re.fullmatch(r'\w+', table):
             raise ValueError(f"Invalid table name: {table}") 
        self.table_name: str = table


    def open(self):
        """Opens a new database connection if one does not exist"""
        if self.conn is None:
            self.conn = sqlite3.connect(f"{self.db_name}")


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
                )""")


    def fetch_all_rows(self) -> list:
        """
        Retrieves all rows from the specified table in the database. 

        Returns:
            A list containing all rows from the table or None if the table 
            doesn't exist.
        """
        with self.conn:
            return self.conn.execute(f"""
                       SELECT * FROM {self.table_name} 
                           ORDER BY timestamp ASC""").fetchall()


    def insert_row(self, row) -> None:
        """
        Inserts a single row into the database. 
        """
        with self.conn: 
            self.conn.execute(f"""
                INSERT OR IGNORE INTO {self.table_name}
                (timestamp, open, high, low, close, volume) 
                VALUES (?, ?, ?, ?, ?, ?)""", row)


    def insert_rows(self, rows) -> None:
        """ 
        Inserts all elements from the passed in list 'rows' variable into the 
        database. 
        """
        with self.conn:
            self.conn.executemany(f"""
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
        with self.conn:
            row = self.conn.execute(f"""
                  SELECT * FROM {self.table_name}
                  ORDER BY timestamp DESC
                  LIMIT 1""").fetchone()
        return row


    def close(self) -> None:
        """Closes an open database connection if one exists"""
        if self.conn:
            self.conn.close()
            self.conn = None 
