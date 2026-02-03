from src.menu.menuInterface import IMenu 
from src.menu.accountMenu import AccountMenu
from src.menu.predictionMenu import PredictionMenu 
from src.menu.automationMenu import AutomationMenu
from src.menu.dashboardMenu import DashboardMenu
from src.menu.maintenanceMenu import MaintenanceMenu
from src.menu.settingsMenu import SettingsMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class MainMenu:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.menus: dict[int, list] = {
            1: ["Manage account", AccountMenu(self.settings)],
            2: ["Make a Prediction", PredictionMenu(self.settings)],
            3: ["Automation Engine", AutomationMenu(self.settings)],
            4: ["Dashboard", DashboardMenu(self.settings)],
            5: ["Maintenance", MaintenanceMenu(self.settings)],
            6: ["Settings", SettingsMenu(self.settings)],
        }


    def run_main_menu(self):
        """ Runs the main menu for the application """
        args: list = (self.settings.username())
        menu_runner(heading, self.menus, main_menu, args)

        print("\033c", end="")
        exit()

        # options = len(self.menus) + 1

        # while True:
        #     print_banner("Algorithmic Trading SYS")
            # dynamic_fprint(main_menu, self.settings.username)
            # for key in self.menus.keys():
            #     print(f"{key}. {self.menus[key][0]}")
            # print(f"{options}. Exit")

            # choice = get_menu_selection(options)
            #
            # if choice == options:
            #     break
            # else:
            #     self.menus[choice][1].run()



heading: str = "Algorithmic Trading SYS"

main_menu: str = \
"""Welcome back {0}, what would you like to do?
"""
