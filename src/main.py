from src.menus.mainMenu import MainMenu 
from src.settings.settings import Settings
from src.engine import Engine 
from src.accountManager import AccountManager
from src.data.dataManager import DataManager

# Temp, get accountmanager to manage its own keys from within on initialization
from src.apiManager import api_key, api_secret

def main():
    settings = Settings()
    account = AccountManager(api_key, api_secret, True)
    data = DataManager(settings)

    engine = Engine(account, data, settings.asset(), settings.timeframe())
    menu = MainMenu(settings, account, engine, data)
    menu.run()


if __name__ == "__main__":
    main()
