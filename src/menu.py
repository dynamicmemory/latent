from src.agent import Agent
from src.sqlitedb import DatabaseManager
import pyfiglet

TIME_MAP: dict[int, str] = {
    1: "15",
    2: "60",
    3: "240",
    4: "D",
    5: "W"
}

ASSET_MAP: dict[int, str] = {
    1: "BTCUSDT",
}


USERNAME:str = "HUMAN OVERLORD"   # Temp

def print_banner(banner_text:str="SYNTRA SYSTEMS") -> None:
    """
    Clears the terminal display and prints a banner for the current menu
           
    Args:
        banner_text: The text to print inside the banner, default to app name.
    """
    print("\033c", end="")
    text = pyfiglet.figlet_format(banner_text, font="slant")
    print(text)
    print("---------------------------------------------------------------")


def print_main_menu() -> int:
    """
    Prints the main menu for the app

    Returns:
        choice: the number of the choice the user has chosen
    """
    print_banner()
    print(f"Welcome back {USERNAME}, what would you like to do?")
    print("1. Manage account")
    print("2. Settings") 
    print("3. Exit")
    print("---------------------------------------------------------------")
    while True:
        try:
            choice = int(input(">> "))
            if choice > 0 and choice < 4:
               break 
            print("Enter a number between 1 - 3")
        except Exception as e:
            print("Enter a number between 1 - 3")
    return choice 


def print_account_menu() -> int:
    return 1;


def print_settings_menu() -> int:
    """
    Prints the settings menu for the app

    Returns:
        choice: the number of the choice the user has chosen
    """
    print_banner("SETTINGS")
    print("Settings")
    print("1. Update database")
    print("2. Retrain Model")
    print("3. Return to main menu")
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


def run_account() -> None:
    pass


def run_settings(choice:int) -> None:
    """
    Runs the settings menu for the application, delegates duties depending 
    on what the user selects to do, current choices are:
      - 1. Updating the database 
      - 2. Retraining the current Model
      - 3. Exiting to the main menu
    """
    if choice == 1:
        for tf in ["15", "60", "240", "D", "W"]:
            dbm = DatabaseManager("BTCUSDT", tf) 
            dbm.update_table()
    elif choice == 2:
        asset:int = 1 
        timeframe:int = 1
        while True:
            try:
                print("Which asset:")
                print("1. Bitcoin")
                asset = int(input(">> "))
                if asset > 0 and asset < 2:
                    break
                print("Enter a number from the provided options.")
            except Exception as e:
                print(f"Only number input will be excepted {e}")


        while True:
            try:
                print("Which timeframe:")
                print("1. 15 minutes")
                print("2. 1 hour")
                print("3. 4 hour")
                print("4. Daily")
                print("5. Weekly")
                timeframe = int(input(">> "))
                if timeframe > 0 and timeframe < 6:
                    break
                print("Enter a number from the provided options")
            except Exception as e:
                print(f"Only number input will be excepted {e}")

        Agent(ASSET_MAP[asset], TIME_MAP[timeframe])
    else:
        return;


def run_menu() -> None:
    """
    Runs the main menu for the application, delegates duties depending 
    on what the user selects to do, current choices are:
      - 1. Check user accounts for managing and trading  
      - 2. Enter the settings menu 
      - 3. Exiting the application
    """
    print_banner()
    choice: int = print_main_menu()
    if int(choice) == 1:
        Agent()
        input("\nHit enter to return to main menu")

    elif int(choice) == 2:
        # Settings menu loop
        while (True):
            choice = print_settings_menu()
            if choice == 3: break
            run_settings(choice)
            input("\nHit enter to continue")

    elif int(choice) == 3:
        print("\033c", end="")
        exit()


if __name__ == "__main__":
    pass    

