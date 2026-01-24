# BEFORE I GET CARRIED AWAY.... YES WE WILL MAKE A MENU MANAGER, JUST FINISH THIS AS IS FOR NOW.
# The menu class is growing at a rapid rate....
from matplotlib.artist import get
from src.exchange import Exchange
from src.engine import Engine
from src.databaseManager import DatabaseManager
from src.accountManager import AccountManager
from src.apiManager import api_key, api_secret
import pyfiglet

USERNAME:str = "HUMAN OVERLORD"   # Temp
TIME_MAP: dict[int, str] = { 1: "15", 2: "60", 3: "240", 4: "D", 5: "W", 0: "None"}
ASSET_MAP: dict[int, str] = { 1: "BTCUSDT", 0: "None"}

def print_banner(banner_text:str="MEMORYVOID") -> None:
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
        if   choice == 1: manage_account()
        elif choice == 2: run_predict()
        elif choice == 3: start_engine() 
        elif choice == 4: stop_engine() 
        elif choice == 5: view_dashboard() 
        elif choice == 6: run_maintenance()
        elif choice == 7: run_settings()  
        elif choice == 8: break

    print("\033c", end="")
    exit()


# TODO: Abstract to separate class to handle account specific printing and input
def manage_account() -> None:
    """ """
    options:int = 6 
    # Temporary Testnet only api keys for development, test net access only
    # Swap to env var once testing complete
    account = AccountManager(api_key=api_key,
                 api_secret=api_secret, 
                 testnet=True)
    # e = Exchange(api_key="KCsB4A1InMGHlCVkoH",
    #              api_secret="jjmP9FrX9gjySQvEguBPYAR2gJd7DKDJJJxj", 
                 # testnet=True)

    while True:
        print_banner("ACCOUNT")
        dynamic_fprint(account_menu)
        choice = get_menu_selection(options)

        if choice == 1: 
            # Refine this into a single call to account
            account.print_all_balances()
            account.print_all_usdt_positions()
            account.print_orders("linear", "BTCUSDT")
        elif choice == 2:
            dynamic_fprint(choose_asset)
            asset = ASSET_MAP[get_menu_selection(1)]
            dynamic_fprint(side_menu)
            side = "Buy" if get_menu_selection(2) == 1 else "Sell"
            size = input("Enter amount: >> ")
            price = input("Enter price: >> ")
            account.create_limit_order(asset, side, size, price)
        elif choice == 3:
            dynamic_fprint(choose_asset)
            asset = ASSET_MAP[get_menu_selection(1)]
            dynamic_fprint(side_menu)
            side = "Buy" if get_menu_selection(2) == 1 else "Sell"
            size = input("Enter amount: >> ")
            account.create_market_order(asset, side, size)
        elif choice == 4:
            dynamic_fprint(choose_asset)
            asset: str = ASSET_MAP[get_menu_selection(1)]
            orders: list|int = account.print_orders("linear", asset)
            if isinstance(orders, int) or len(orders) == 0:
                continue
            print("Select the 'No' of the order you want to cancel")
            order_id: int = get_menu_selection(len(orders))
            account.cancel_order("linear", asset, orders[order_id-1])
        elif choice == 5:
            account.cancel_all_USDT_orders("linear")
        elif choice == 6:
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
                agent:Engine = Engine(ASSET_MAP[asset], TIME_MAP[timeframe])
                agent.run_agent(f"./models/{ASSET_MAP[asset]}-{TIME_MAP[timeframe]}-model.pth")
                input("\n>> Hit enter to continue")

        elif choice == 4:
            break


def start_engine() -> None:
    """ 


    """
    options:int = 5
    asset:int = 0
    engine_status = None
    timeframe:int = 0
    while True:
        print_banner("AUTOMATION")
        dynamic_fprint(start_menu, engine_status, ASSET_MAP[asset], TIME_MAP[timeframe])
        choice:int = get_menu_selection(options)
        if choice == 1:
            if asset == 0 or timeframe == 0:
                print("\nError: Select an asset and timeframe to predict on first")
                input("\nHit enter to continue")
                continue
            # Engine is currently always none and start engine isnt built yet 
            # so this is fine for now.
            if engine_status is not None:
                print("Engine is already running...")
                input("\nHit enter to continue")
                continue

            print("Feature currently under construction")
            input("\nHit enter to continue")

        elif choice == 2:
            dynamic_fprint(pred_asset)
            asset = get_menu_selection(len(ASSET_MAP))
        elif choice == 3:
            dynamic_fprint(pred_timeframe)
            timeframe = get_menu_selection(len(TIME_MAP))
        elif choice == 4:
            print("Feature currently under construction")
            input("\nHit enter to continue")
        elif choice == 5:
            break 


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
                dbm.export_csv()
            input("\n>> Hit enter to continue")
        elif choice == 2:
            # Combined with whats in the agent class, this should move to a 
            # retraining class that can simply be called from here, and which 
            # calls whichever algos/model building it needs from within the class.
            agent = Engine()
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
            agent = Engine(a, t)
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
1. Account overview 
2. Place limit order 
3. Place market order 
4. Cancel order 
5. Cancel all orders
6. Return to main menu"""

choose_asset: str = """
Which asset:
1. Bitcoin"""

side_menu: str = """
Which side:
1. Buy
2. Sell"""

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
Engine is currently {0} | Current Asset: {1} | Current Timeframe: {2}\n 
1. Start Engine 
2. Choose asset 
3. Choose timeframe
4. Check health
5. Return to main menu 
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
