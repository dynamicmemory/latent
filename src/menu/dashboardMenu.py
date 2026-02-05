from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class DashboardMenu(IMenu):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.menu: dict[int, list] = {
            1: ["Launch Dashboard", self.dashboard],
        }


    def run(self) -> None:
        menu_runner(title, self.menu, header, lambda: [])


    def dashboard(self) -> None:
        print("The engineer is currently working on it!") 


title: str = "Dashboard"
header: str = ""

