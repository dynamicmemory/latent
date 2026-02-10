from src.data.dataManager import DataManager
from src.engine.engine import Engine
from src.menus.menuInterface import IMenu
from src.menus.menuUtilities import *
from src.settings.settings import Settings

class PredictionMenu(IMenu):
    def __init__(self, settings: Settings, engine: Engine, data: DataManager):
        self.settings = settings
        self.engine = engine
        self.data = data
        self.menu: dict[int, list] = {
            1: ["Make a prediction", self.predict],
            2: ["Change Asset", self.change_asset],
            3: ["Change Timeframe", self.change_timeframe],
        }

    def run(self) -> None:
        menu_runner(title, self.menu, header, lambda: [
            self.settings.asset(),
            self.settings.timeframe()
        ])


    # engine should not own manual prediction it belongs with the model in a 
    # separate class or model manager and should be a callable function from here.
    def predict(self) -> None:
        asset = self.settings.asset()
        timeframe = self.settings.timeframe()
        self.engine.manual_prediction(asset, timeframe)
        input("\nHit enter to continue")


    def change_asset(self) -> None:
        asset = choose_asset()
        timeframe = self.settings.timeframe()
        self.settings.save_asset(asset)
        self.data.update_data(asset, timeframe)
        input("\nHit enter to continue")
         

    def change_timeframe(self) -> None:
        timeframe = choose_timeframe()
        asset = self.settings.asset()
        self.settings.save_timeframe(timeframe)
        self.data.update_data(asset, timeframe)
        input("\nHit enter to continue")


title: str = "Make A Prediction"
header: str = "Current Asset: {0} | Current Timeframe: {1}\n"
