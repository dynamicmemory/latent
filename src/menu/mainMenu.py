from src.menu.accountMenu import AccountMenu
from src.menu.predictionMenu import PredictionMenu 
from src.menu.automationMenu import AutomationMenu
from src.menu.dashboardMenu import DashboardMenu
from src.menu.maintenanceMenu import MaintenanceMenu
from src.menu.settingsMenu import SettingsMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings
from src.accountManager import AccountManager
from src.engine import Engine

class MainMenu:
    def __init__(self, settings: Settings, account: AccountManager, engine: Engine) -> None:
        self.settings = settings
        self.account = account 
        self.engine = engine
        self.menus: dict[int, list] = {
            1: ["Manage account", AccountMenu(self.settings, self.account).run],
            2: ["Make a Prediction", PredictionMenu(self.settings).run],
            3: ["Automation Engine", AutomationMenu(self.settings).run],
            4: ["Dashboard", DashboardMenu(self.settings).run],
            5: ["Maintenance", MaintenanceMenu(self.settings, self.engine).run],
            6: ["Settings", SettingsMenu(self.settings).run],
        }


    def run_main_menu(self):
        """ Runs the main menu for the application """
        args: list = [self.settings.username()]
        menu_runner(heading, self.menus, main_menu, args)

        print("\033c", end="")
        exit()


heading: str = "Algorithmic Trading SYS"

main_menu: str = \
"""Welcome back {0}, what would you like to do?
"""
