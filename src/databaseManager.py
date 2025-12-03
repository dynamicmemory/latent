from __future__ import annotations
from typing import TYPE_CHECKING
from src.database import Database as database
from src.paths import get_data_path
import pandas as pd 

if TYPE_CHECKING:
    from database import Database
    from exchange import Exchange


class DatabaseManager:

    def __init__(self, fname: str, timeframe: str, exchange: Exchange):
        self.db: Database = database(fname, timeframe)
        self.exchange: Exchange = exchange 
        self.path = get_data_path(fname)


    # TODO: This is so broken of logic, serious rewrite of this class
    def update_db(self) -> pd.DataFrame:
        # Create db and exchange instances 
        db: Database = self.db
        ex: Exchange = self.exchange

        # TODO: Rewrite the check for the db here outside of the db class 
        # Check if db exists yet, pass in the maximum rows from the exchange
        db.create_db(ex.get_ohlc())

        # Calculate how many records are missing 
        db.read_records()
        record_numbers: int = db.find_multiples() + 1
        # Request that number of records from the exchange  + 1 for the delete 
        records = ex.get_ohlc(record_numbers)

        # Update the db with the missing record(s).
        db.update_records(records)


    def get_data(self) -> pd.DataFrame:
        """
        Temporary class for returning a df from the db, need to add cleaning, 
        time calcs, everything that would get the dataframe ready to calculate 
        math on 
        """
        return pd.read_csv(self.path)

