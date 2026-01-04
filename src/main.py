# TODO: Ensure asset name and timeframe are checked for safety b4 db access
from src.agent import Agent
from src.sqlitedb import DatabaseManager
import sys
import pyfiglet

def print_banner() -> None:
    print("\033c", end="")
    text = pyfiglet.figlet_format("SYNTRA", font="slant")
    print(text)
    print("----------------------------------------")


def print_menu() -> int:
    print("Welcome back <username>, what would you like to do?")
    print("1. Manage account")
    print("2. Update database") 
    print("3. Exit")
    print("----------------------------------------")
    while True:
        try:
            choice = int(input(">> "))
            if choice > 0 and choice < 4:
               break 
            print("Enter a number between 1 - 3")
        except Exception as e:
            print("Enter a number between 1 - 3")
    return choice 


def run_menu() -> None:
    print_banner()
    choice: int = print_menu()
    if int(choice) == 1:
        print_banner()
        Agent()
        input("\nHit enter to return to main menu")

    elif int(choice) == 2:
        print_banner()
        for tf in ["15", "60", "240", "D", "W"]:
            dbm = DatabaseManager("BTCUSDT", tf) 
            dbm.update_table()
        input("\nHit enter to return to main menu")

    elif int(choice) == 3:
        print_banner()
        print("\033c", end="")
        exit()


def main():
    while True:
        run_menu()


if __name__ == "__main__":
    main()
    



