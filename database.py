# TODO: Rewrite using a csv or better yet use sqlite

import os as os 
import csv 

class Database:

    def __init__(self, symbol: str, interval: str) -> None:
        self.symbol: str = symbol
        self.interval: str= interval 
        self.fname: str = f"{self.symbol}-{self.interval}.txt"
        self.lines: list = []


    # TODO: Build file creation logic and header checking logic 
    def create_db(self) -> None:
        """ 
        Checks directory for an existing db file, creates one if it doesn't 
        exist, checks to make sure the file has correct headers 
        """ 
        if not self.fname:
            pass 
        else:
            pass 

   
    def read_records(self) -> None:
        """ 
        Reads all lines from the db file and stores them under 'lines'
        """
        # with open(self.fname, 'r') as file:
        #     self.lines = file.readlines()
        with open(self.fname, 'r') as file:
            reader = csv.reader(file, delimiter=",")
            for line in reader:
                self.lines.append(line)

    def write_records(self, lines: list, n: int=1000) -> None:
        """ 
        Write 'n' number of lines into the db file. 
        Param: n - int number of lines to write in.
        """
        # with open(self.fname, 'a') as file:
        #     exchange = []    # I need to make an exchange obj
        #     file.writelines(exchange)
        #     self.read_records()       # Update the lines store from the db
        with open(self.fname, 'a') as file:
            writer = csv.writer(file)
            writer.writerows(lines)
            # exchange = []    # I need to make an exchange obj
            # file.writelines(exchange)
            # self.read_records()       # Update the lines store from the db
            #

    def delete_records(self) -> None:
        """ 
        Deletes the last line in the db. 
        """
        with open(self.fname, 'w') as file:
            file.writelines(self.lines[:-1])


    def update_records(self, n: int) -> None:
        """ 
        Updates the db with 'n' number of lines.
        Param: n - int number of lines to update the db with
        """
        self.create_db()
        self.delete_records()
        self.write_records(n)


    # DATA CLEANING
    # calc time
    # 
    # Get price
