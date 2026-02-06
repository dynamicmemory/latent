from src.engine import Engine
from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class PredictionMenu(IMenu):
    def __init__(self, settings: Settings, engine: Engine):
        self.settings = settings
        self.engine = engine
        self.menu: dict[int, list] = {
            1: ["Make a prediction", self.predict],
            2: ["Change Asset", self.change_asset],
            3: ["Change Timeframe", self.change_timeframe],
        }

    def run(self) -> None:
        menu_runner(title, self.menu, header, lambda: [
            asset_tostring(self.settings.asset()),
            timeframe_tostring(self.settings.timeframe())
        ])


    # engine should not own manual prediction it belongs with the model in a 
    # separate class or model manager and should be a callable function from here.
    def predict(self) -> None:
        asset = asset_tostring(self.settings.asset())
        timeframe = timeframe_tostring(self.settings.timeframe())
        self.engine.manual_prediction(f"./pickled_models/{asset}-{timeframe}-model.pth")


    def change_asset(self) -> None:
        self.settings.save_asset(choose_asset())
        print("Asset has been updated")


    def change_timeframe(self) -> None:
        self.settings.save_timeframe(choose_timeframe())
        print("Timeframe has been updated")
        

title: str = "Make A Prediction"
header: str = "Current Asset: {0} | Current Timeframe: {1}\n"
