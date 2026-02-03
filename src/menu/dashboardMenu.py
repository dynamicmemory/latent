from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class DashboardMenu(IMenu):
    def __init__(self, settings: Settings):
        self.settings = settings


    def run(self) -> None:
        pass


# def view_dashboard() -> None:
#     print("Feature currently under construction")
#     input("\nHit enter to continue")
#     pass
