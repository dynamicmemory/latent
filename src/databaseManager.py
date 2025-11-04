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
        # Create db and exchange instances 
        db: Database = self.db
        ex: Exchange = self.exchange

        # TODO: Rewrite the check for the db here outside of the db class 
        # Check is db exists yet, pass in the maximum rows from the exchange
        db.create_db(ex.get_ohlc())

        # Calculate how many records are missing 
        db.read_records()
        record_numbers: int = db.find_multiples() + 1
        # Request that number of records from the exchange  + 1 for the delete 
        records = ex.get_ohlc(record_numbers)

        # Update the db with the missing record(s).
        db.update_records(records)

