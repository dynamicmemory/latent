from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class AutomationMenu(IMenu):
    def __init__(self, settings: Settings):
        self.settings = settings


    def run(self) -> None:
        pass





# def start_engine() -> None:
#     """ Menu for running the main automation engine """
#     options:int = 6
#     asset:int = settings.default_asset() 
#     timeframe:int = settings.default_timeframe() 
#
#     engine_status = settings.automation_engine()
#     if engine_status is None:
#         AUTOMATION_ENGINE = Engine(ASSET_MAP[asset], TIME_MAP[timeframe])
#
#     while True:
#         print_banner("AUTOMATION")
#         dynamic_fprint(automate_menu, engine_status, ASSET_MAP[asset], TIME_MAP[timeframe])
#         choice:int = get_menu_selection(options)
#         if choice == 1:
#             if engine_status is not None:
#                 print("Engine is already running...")
#                 input("\nHit enter to continue")
#                 continue
#
#             if asset == 0 or timeframe == 0:
#                 print("\nError: Select an asset and timeframe to predict on first")
#                 input("\nHit enter to continue")
#                 continue
#
#             AUTOMATION_ENGINE.start_automation()
#             settings.save_engine("Running")
#
#             input("\nHit enter to continue")
#
#         elif choice == 2:
#             dynamic_fprint(choose_asset_menu)
#             asset = get_menu_selection(len(ASSET_MAP)-1)
#             settings.save_asset(asset)
#         elif choice == 3:
#             dynamic_fprint(timeframe_menu)
#             timeframe = get_menu_selection(len(TIME_MAP)-1)
#             settings.save_timeframe(timeframe)
#         elif choice == 4:
#             print("Feature currently under construction")
#             input("\nHit enter to continue")
#
#         elif choice == 5:
#             if settings.automation_engine() is None:
#                 print("Engine currently not running")
#                 input("\nHit enter to continue")
#                 continue 
#             AUTOMATION_ENGINE.stop_automation()
#             settings.save_engine(None)
#
#             input("\nHit enter to continue")
#         elif choice == 6:
#             break 
