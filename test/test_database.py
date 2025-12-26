from src.sqlitedb import DatabaseManager,  Database


def init_database():
    db = Database(":memory:", "test_table")
    db.create_table()
    return db


def test_create_table():
    db = init_database()
    tables = db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'").fetchall()

    assert("test_table",) in tables, "Table was not created"  
    

def test_fetch_all():
    db = init_database()

    # Test no rows 
    number_of_rows = db.fetch_all_rows()
    assert len(number_of_rows) == 0, "There should be 0 rows"

    # Test one row
    row = [1,2,3,4,5,6]
    db.conn.execute(
        """INSERT INTO test_table
            (timestamp, open, high, low, close, volume) 
            VALUES (?, ?, ?, ?, ?, ?)""", row)

    number_of_rows = db.fetch_all_rows()
    assert len(number_of_rows) == 1, "There should be 1 row"


def test_insert_rows():
    db = init_database()

    rows = [ 
        (1000,2,3,4,5,10),
        (1000,2,3,4,5,10),
    ]

    db.insert_rows(rows)
    number_of_rows = db.fetch_all_rows()

    assert len(number_of_rows) == 1, "There should only be 1 row"


def test_latest_rows():
    db = init_database()

    rows = [ 
        (1000,2,3,4,5,10),
        (2000,2,3,4,5,10),
    ]

    db.insert_rows(rows)
    row = db.get_latest_row()

    assert row[0] == 2000, "Lastest timestamp is not 2000"



def test_calculate_missing_rows():
    pass 


def update_table_test():
    db = init_database()
    pass 

def get_dataframe_test():
    db = init_database()
    pass
