# TODO: Move helper files to dbms class
# TODO: Pivot to SQLite db once software works end to end.
import os as os 
import datetime as dt
import csv
from pathlib import Path
from src.paths import get_data_path

class Database:
    def __init__(self, fname: str, timeframe: str) -> None:
        self.fname: str = fname
        self.timeframe: str = timeframe
        self.path = get_data_path(fname)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lines: list = []


#    ---- Database Operations -----

    # TODO: Change hard coded header into more modular solution 
    def create_db(self, records: list) -> None:
        """ 
        Checks directory for an existing db file, creates one if it doesn't 
        exist, checks to make sure the file has correct headers 
        """ 
        headers: list = [["utc","date","time","open","high","low","close","volume"]]
        if not self.path.exists(): 
            self.write_headers(headers)
            self.write_records(records)
        else:
            self.read_records()
            if len(self.lines) == 0:
                self.write_headers(headers)
                self.write_records(records)


    def read_records(self) -> None:
        """ 
        Reads all lines from the db file and stores them under 'lines'
        """
        with self.path.open('r') as file:
            reader = csv.reader(file, delimiter=",")
            self.lines = []      # Always reset rows before rereading the db
            for line in reader:
                self.lines.append(line)


    # TODO: Currently not using length at all  
    # TODO: Redo line writing logic
    def write_records(self, lines: list, n: int=1000) -> None:
        """ 
        Write 'n' number of lines into the db file. 
        Param: n - int number of lines to write in.
        """
        with self.path.open('a') as file:
            writer = csv.writer(file)
            for line in lines:
                date, time = self.convert_time(line[0]) 
                writer.writerow([line[0],date,time,line[1],line[2],line[3],line[4],line[6]])


    def delete_records(self) -> None:
        """ 
        Deletes the last line in the db. 
        """
        with self.path.open('w') as file:
            writer = csv.writer(file)
            rows = []
            
            for line in self.lines[:-1]:
                rows.append(line) 
            writer.writerows(rows)


    def update_records(self, records: list, n: int=0) -> None:
        """ 
        Updates the db with 'n' number of lines.
        Param: n - int number of lines to update the db with
        """
        self.read_records()
        self.delete_records()
        self.write_records(records)


    # ---------- HELPERS THAT SHOULD PROBABLY MOVE CLASSES -------------


    def write_headers(self, headers: list) -> None:
        """
        Writes the headings/column names for a csv
        """
        with self.path.open('a') as file:
            writer = csv.writer(file)
            writer.writerows(headers)


    def convert_time(self, time: str) -> tuple:
        """
        Params: utc string 
        """
        convert: float = int(time) / 1000
        temp = str(dt.datetime.fromtimestamp(convert, tz=dt.timezone.utc))

        # Current format XXXX/XX/XX XX:XX:XX+XX:XX we must break it up
        split_str: list = temp.split(" ")
        d: str = split_str[0]
        t: str = split_str[1].split("+")[0]

        return d, t


    def find_multiples(self) -> int:
        """
        Calculates the number of records missing according to utc 
        Returns the amount as an int
        """
        # convert exchange api times to actual minutes for unix conversions
        time_map: dict = {"15": 15,
                          "60": 60,
                          "240": 240,
                          "D": 1440,
                          "W": 10080}

        # Get the current time 
        current_time = dt.datetime.now(dt.timezone.utc).timestamp()*1000
        print(f"Current time {current_time}")

        # # Get the time from the last record
        last_rec_time = self.lines[-1][0].split(",")[0]
        print(f"Last record time {last_rec_time}")
        
        # # Get the difference between the two 
        time_diff = int(current_time) - int(last_rec_time)
        print(f"Time difference {time_diff}")

        # *60000 is number of ms in a minute, * by number of mins in timeframe
        tf_milliseconds = time_map[self.timeframe] * 60000
        print(f"Timeframe time {tf_milliseconds}")

        # # Find out how many multiples of the Timeframe is missing from records 
        multiples = time_diff // tf_milliseconds
        print(f"Mutliples missing {multiples}")
        
        return multiples
