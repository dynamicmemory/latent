import sqlite3
import os as os 
import datetime as dt


class Database:
    def __init__(self, db_name:str, table:str) -> None:
        """
        Initializes the database class.

        Args:
            db_name: name of the database being queried.
            table: the name of the table being queried.
        """
        self.conn: sqlite3.Connection = sqlite3.connect(f"{db_name}.db")
        self.cur: sqlite3.Cursor = self.conn.cursor()
        self.table = table


    def create_db(self) -> None:
        """ 
        Creates a table using the table name passed into the database 
        constructor if that table does not exist.
        """
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
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
        self.database.create_db() 




