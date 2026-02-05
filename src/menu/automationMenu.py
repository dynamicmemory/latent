from src.engine import Engine
from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings
from enum import Enum

class AutoStatus(Enum):
    NONE = None
    RUNNING = "running"


class AutomationMenu(IMenu):
    def __init__(self, settings: Settings, engine: Engine):
        self.settings = settings
        self.engine = engine
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
            asset_tostring(self.settings.asset()),
            timeframe_tostring(self.settings.timeframe())
        ])


    def start_engine(self) -> None:
        if self.settings.automation_status() is None:
            self.engine.start_automation()
            self.settings.save_automation_status(AutoStatus.RUNNING.value)
            return
        print("Automation is already running...")

    
    def stop_engine(self) -> None:
        if self.settings.automation_status() is not None:
            self.engine.stop_automation()
            self.settings.save_automation_status(AutoStatus.NONE.value)
            return 
        print("Automation is currently turned off...")


    def check_health(self) -> None:
        print("Feature under construction")


    def change_asset(self) -> None:
        self.settings.save_asset(choose_asset())
         

    def change_timeframe(self) -> None:
        self.settings.save_timeframe(choose_timeframe())


title: str = "Automation Engine"
header: str = "Automation is {0} | Asset - {1} | Timeframe - {2}\n"
