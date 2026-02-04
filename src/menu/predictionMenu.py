from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class PredictionMenu(IMenu):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.menu: dict[int, list] = {
            # 1: ["", self.],
            # 2: ["", self.],
            # 3: ["", self.],
            # 4: ["", self.],
        }

    def run(self) -> None:
        args: list = []
        menu_runner(title, self.menu, header, args)


title: str = ""
header: str = ""

#
# def run_predict() -> None:
#     options:int = 4 
#     asset:int = 0
#     timeframe:int = 0
#     while True:
#         print_banner("PREDICTION")
#         dynamic_fprint(pred_menu, ASSET_MAP[asset], TIME_MAP[timeframe])
#
#         choice = get_menu_selection(options)
#         if choice == 1:
#             dynamic_fprint(choose_asset_menu)
#             asset = get_menu_selection(len(ASSET_MAP)-1)
#
#         elif choice == 2:
#             dynamic_fprint(timeframe_menu)
#             timeframe = get_menu_selection(len(TIME_MAP)-1)
#
#         elif choice == 3:
#             if asset == 0 or timeframe == 0:
#                 print("\nError: Select an asset and timeframe to predict on first")
#                 input("\n>> Hit enter to continue")
#                 continue
#             else:
#                 agent:Engine = Engine(ASSET_MAP[asset], TIME_MAP[timeframe])
#                 agent.manual_prediction(f"./models/{ASSET_MAP[asset]}-{TIME_MAP[timeframe]}-model.pth")
#                 input("\n>> Hit enter to continue")
#
#         elif choice == 4:
#             break
#
#
#
