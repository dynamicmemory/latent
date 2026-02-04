# from src.menus import run_main_menu
from src.menu.mainMenu import MainMenu 
from src.settings.settings import Settings
from src.engine import Engine 
from src.accountManager import AccountManager

# Temp, get accountmanager to manage its own keys from within on initialization
from src.apiManager import api_key, api_secret

def main():
    settings = Settings()
    account = AccountManager(api_key, api_secret, True)

    # TODO: Use settings to initialize asset and tf vals 
    engine = Engine(account)

    menu = MainMenu(settings, account, engine)
    menu.run_main_menu()
    # run_main_menu()


if __name__ == "__main__":
    main()
