# BEFORE I GET CARRIED AWAY.... YES WE WILL MAKE A MENU MANAGER, JUST FINISH THIS AS IS FOR NOW.
from src.exchange import Exchange
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
    """ """
    options:int = 3 

    while True:
        print_banner("ACCOUNT")
        dynamic_fprint(account_menu)
        choice = get_menu_selection(options)

        # Temporary Testnet only api keys for development, test net access only
        # Swap to env var once testing complete
        if choice == 1: 
            e = Exchange(api_key="KCsB4A1InMGHlCVkoH",
                 api_secret="jjmP9FrX9gjySQvEguBPYAR2gJd7DKDJJJxj", 
                 testnet=True)
            
            e.get_all_balances()
        elif choice == 2:
            e = Exchange(api_key="KCsB4A1InMGHlCVkoH",
                 api_secret="jjmP9FrX9gjySQvEguBPYAR2gJd7DKDJJJxj", 
                 testnet=True)
            print(e.get_position())
        elif choice == 3:
            break 
        
        input("\n>> Hit enter to continue")


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
            if asset == 0 or timeframe == 0:
                print("\nError: Select an asset and timeframe to predict on first")
                input("\n>> Hit enter to continue")
                continue
            else:
                agent = Agent(ASSET_MAP[asset], TIME_MAP[timeframe])
                agent.run_agent(f"./models/{ASSET_MAP[asset]}-{TIME_MAP[timeframe]}-model.pth")
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
            agent = Agent()
            mod = agent.list_models("./models")
            agent.print_models(mod)

            # print(len(mod))
            if len(mod) == 0:
                print("\nThere are no models to retrain, go create one... blah blah.")
                return;

            print("\nWhich model would you like to retrain\n")
            model = get_menu_selection(len(mod)+1)
            if model == len(mod)+1:
                break

            choosen_model = mod[model-1]['name']
            a = choosen_model.split("-")[0]
            t = choosen_model.split("-")[1]
            agent = Agent(a, t)
            agent.retrain(f"./models/{a}-{t}-model.pth")
                
            input("\n>> Hit enter to continue")
        else:
            return;


# Global settings for the program, make these persistance with a config file
def run_settings() -> None:
    options:int = 5
    while True:
        print_banner("SETTINGS")
        dynamic_fprint(settings_menu)
        choice = get_menu_selection(options)

        if choice != 5:
            print("Feature currently under construction")
            input("\nHit enter to continue")
        else:
            return;


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

account_menu: str = """
1. Show account balance 
2. Show open positions
3. Return to main menu"""

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
1. Change account name
2. Manage API keys
3. Scheduler
4. Preferences
5. Return to main menu
"""
