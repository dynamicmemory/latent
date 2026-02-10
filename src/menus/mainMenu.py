from src.data.dataManager import DataManager
from src.menus.accountMenu import AccountMenu
from src.menus.predictionMenu import PredictionMenu 
from src.menus.automationMenu import AutomationMenu
from src.menus.dashboardMenu import DashboardMenu
from src.menus.maintenanceMenu import MaintenanceMenu
from src.menus.settingsMenu import SettingsMenu
from src.menus.menuUtilities import *
from src.settings.settings import Settings
from src.account.accountManager import AccountManager
from src.engine.engine import Engine

class MainMenu:
    def __init__(self, settings: Settings, account: AccountManager, engine: Engine, data: DataManager) -> None:
        self.settings = settings
        self.account = account 
        self.engine = engine
        self.data = data
        self.menus: dict[int, list] = {
            1: ["Manage account", AccountMenu(self.settings, self.account, self.data).run],
            2: ["Make a Prediction", PredictionMenu(self.settings, self.engine, self.data).run],
            3: ["Automation Engine", AutomationMenu(self.settings, self.engine, self.data).run],
            4: ["Dashboard", DashboardMenu(self.settings).run],
            5: ["Maintenance", MaintenanceMenu(self.settings, self.engine).run],
            6: ["Settings", SettingsMenu(self.settings).run],
        }


    def run(self):
        """ Runs the main menu for the application """
        menu_runner(heading, self.menus, main_menu, lambda: [
            self.settings.username()
        ])

        print("\033c", end="")
        exit()


heading: str = "  Latent Systems"

main_menu: str = \
"""Welcome back {0}, what would you like to do?
"""
