from src.menus.menuInterface import IMenu
from src.menus.menuUtilities import *
from src.settings.settings import Settings

class SettingsMenu(IMenu):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.menu: dict[int, list] = {
            1: ["Update username", self.username],
            2: ["Edit scheduling", self.scheduler],
            # 3: ["", self.],
        }


    def run(self) -> None:
        menu_runner(title, self.menu, header, lambda: [])


    def username(self) -> None:
        name = input("Enter new Username\n\n>> ")
        self.settings.save_username(name)
        input("\nHit enter to continue")


    def scheduler(self) -> None:
        print("Feature currently under construction")
        input("\nHit enter to continue")
    

title: str = "System Settings"
header: str = ""
