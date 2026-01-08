# BEFORE I GET CARRIED AWAY.... YES WE WILL MAKE A MENU MANAGER, JUST FINISH THIS AS IS FOR NOW.
from src.agent import Agent
from src.sqlitedb import DatabaseManager
import pyfiglet

USERNAME:str = "HUMAN OVERLORD"   # Temp
TIME_MAP: dict[int, str] = { 1: "15", 2: "60", 3: "240", 4: "D", 5: "W", 0: "None"}
ASSET_MAP: dict[int, str] = { 1: "BTCUSDT", 0: "None"}

def print_banner(banner_text:str="SYNTRA SYSTEMS") -> None:
    """
    Clears the terminal display and prints a banner for the current menu
           
    Args:
        banner_text: The text to print inside the banner, default to app name.
    """
    print("\033c", end="")
    text = pyfiglet.figlet_format(banner_text, font="slant")
    print(text)
    print("-"*60)


def dynamic_fprint(template:str, *args):
    print(template.format(*args))

    
def get_menu_selection(options:int) -> int:
    """ Returns the selected menu item """
    print("-"*60)
    while True:
        try:
            choice = int(input("\n>> "))
        except (ValueError, TypeError):
            print("Enter a number from the provided options")
            continue

        if choice > 0 and choice < options+1:
            return choice 
        print("Enter a number from the provided options")


def run_main_menu() -> None:
    """ Runs the main menu for the application """
    options:int = 8
    while True:
        print_banner()
        dynamic_fprint(main_menu, USERNAME)
        choice = get_menu_selection(options)

        # TODO: Change to a dict and run choice from the dict
        if   choice == 1: manage_accout()
        elif choice == 2: run_predict()
        elif choice == 3: start_engine() 
        elif choice == 4: stop_engine() 
        elif choice == 5: view_dashboard() 
        elif choice == 6: run_maintenance()
        elif choice == 7: run_settings()  
        elif choice == 8: break

    print("\033c", end="")
    exit()


def manage_accout() -> None:
    print("Feature currently under construction")
    input("\nHit enter to continue")
    pass


def run_predict() -> None:
    options:int = 4 
    asset:int = 0
    timeframe:int = 0
    while True:
        print_banner("PREDICTION")
        dynamic_fprint(pred_menu, ASSET_MAP[asset], TIME_MAP[timeframe])

        choice = get_menu_selection(options)
        if choice == 1:
            dynamic_fprint(pred_asset)
            asset = get_menu_selection(len(ASSET_MAP))

        elif choice == 2:
            dynamic_fprint(pred_timeframe)
            timeframe = get_menu_selection(len(TIME_MAP))

        elif choice == 3:
            if asset is 0 or timeframe is 0:
                print("\nError: Select an asset and timeframe to predict on first")
                input("\n>> Hit enter to continue")
                continue
            else:
                Agent(ASSET_MAP[asset], TIME_MAP[timeframe])
                input("\n>> Hit enter to continue")

        elif choice == 4:
            break


def start_engine() -> None:
    print("Feature currently under construction")
    input("\nHit enter to continue")
    pass
def stop_engine() -> None:
    print("Feature currently under construction")
    input("\nHit enter to continue")
    pass
def view_dashboard() -> None:
    print("Feature currently under construction")
    input("\nHit enter to continue")
    pass


def run_maintenance() -> None:
    """ Runs the maintenance menu for the application """
    options:int = 3
    while True:
        print_banner("MAINTENANCE")
        dynamic_fprint(maintenance_menu)
        choice = get_menu_selection(options)

        if choice == 1:
            for tf in ["15", "60", "240", "D", "W"]:
                dbm = DatabaseManager("BTCUSDT", tf) 
                dbm.update_table()
            input("\n>> Hit enter to continue")
        elif choice == 2:
            # Print out a list of all models and the last time they were updated
            # Allow retraining on any or model
            print("Feature currently under construction")
            input("\n>> Hit enter to continue")
        else:
            return;


# Global settings for the program, make these persistance with a config file
def print_settings_menu() -> None:
    """ Prints the settings menu for the app """
    print_banner("SETTINGS")
    print("1. Change account name")
    print("2. Manage API keys")
    print("3. Scheduler")
    print("4. Preferences")
    print("5. Return to main menu")


def run_settings() -> None:
    print("Feature currently under construction")
    input("\nHit enter to continue")
    pass


if __name__ == "__main__":
    pass


# Menu strings
main_menu: str = \
"""Welcome back {0}, what would you like to do?\n
1. Manage account
2. Predict (manual)
3. Start engine
4. Stop engine
5. View Dashboard
6. Maintenance
7. Settings
8. Exit"""

account_menu: str = """"""

pred_menu: str = \
"""Current Asset: {0} | Current Timeframe: {1}\n
1. Choose asset
2. Choose timeframe
3. Make a prediction
4. Return to main menu"""

pred_asset: str = """
Which asset:
1. Bitcoin"""

pred_timeframe: str = """
Which timeframe:
1. 15 minutes
2. 1 hour
3. 4 hour
4. Daily
5. Weekly"""

start_menu: str = """
"""

stop_menu: str = """
"""

dashboard_menu: str = """
"""

maintenance_menu: str = \
"""Maintenance menu\n
1. Update database
2. Retrain models
3. Return to main menu"""

settings_menu: str = """
"""
