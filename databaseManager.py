from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database import Database
    from exchange import Exchange


class DatabaseManager:

    def __init__(self, db, exchange):
        self.db: Database = db 
        self.exchange: Exchange = exchange 


    def update_db(self):
        db: Database = self.db
        ex: Exchange = self.exchange
        # Check if db file exists from the file name the exchange gives us 
        records = ex.get_ohlc()
        db.create_db(records)
        # Sort control paths for create file 

        # Calculate how many records are missing 
        db.read_records()
        record_numbers: int = db.find_multiples() + 1
        # Request that number of records from the exchange  + 1 for the delete 
        records = ex.get_ohlc(record_numbers)
        # call write for the db with that number.
        db.update_records(records, record_numbers)
        pass 

