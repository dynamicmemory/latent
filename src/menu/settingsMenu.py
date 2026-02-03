from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class SettingsMenu(IMenu):
    def __init__(self, settings: Settings):
        self.settings = settings
    

    def run(self) -> None:
        pass




# Global settings for the program, make these persistance with a config file
# def run_settings() -> None:
#     options:int = 5
#     while True:
#         print_banner("SETTINGS")
#         dynamic_fprint(settings_menu)
#         choice = get_menu_selection(options)
#
#         if choice != 5:
#             print("Feature currently under construction")
#             input("\nHit enter to continue")
#         else:
#             return;
#
#
