from src.data.dataManager import DataManager
from src.engine.engine import Engine
from src.menus.menuInterface import IMenu
from src.menus.menuUtilities import *
from src.settings.settings import Settings
from enum import Enum

class AutoStatus(Enum):
    NONE = None
    RUNNING = "running"


class AutomationMenu(IMenu):
    def __init__(self, settings: Settings, engine: Engine, data: DataManager):
        self.settings = settings
        self.engine = engine
        self.data = data
        self.menu: dict[int, list] = {
            1: ["Start Automation", self.start_engine],
            2: ["Stop Automation", self.stop_engine],
            3: ["Check health", self.check_health],
            4: ["Change timeframe", self.change_asset],
            5: ["Change Asset", self.change_timeframe],
        }


    def run(self) -> None:
        menu_runner(title, self.menu, header, lambda: [
            self.settings.automation_status(),
            self.settings.asset(),
            self.settings.timeframe()
        ])


    def start_engine(self) -> None:
        if self.settings.automation_status() is None:
            self.engine.start_automation()
            self.settings.save_automation_status(AutoStatus.RUNNING.value)
            input("\nHit enter to continue >> ")
            return
        print("Automation is already running...")
        input("\nHit enter to continue >> ")

    
    def stop_engine(self) -> None:
        if self.settings.automation_status() is not None:
            self.engine.stop_automation()
            self.settings.save_automation_status(AutoStatus.NONE.value)
            return 
        print("Automation is currently turned off...")
        input("\nHit enter to continue >> ")


    def check_health(self) -> None:
        print("Feature under construction")
        input("\nHit enter to continue >> ")


    def change_asset(self) -> None:
        asset = choose_asset()
        timeframe = self.settings.timeframe()
        self.settings.save_asset(asset)
        self.data.update_data(asset, timeframe)
        input("\nHit enter to continue >> ")
         

    def change_timeframe(self) -> None:
        timeframe = choose_timeframe()
        asset = self.settings.asset()
        self.settings.save_timeframe(timeframe)
        self.data.update_data(asset, timeframe)
        input("\nHit enter to continue >> ")


title: str = "Automation Engine"
header: str = "Automation is {0} | Asset - {1} | Timeframe - {2}\n"
