from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class MaintenanceMenu(IMenu):
    def __init__(self, settings: Settings):
        self.settings = settings



    def run(self) -> None:
        pass



#
# def run_maintenance() -> None:
#     """ Runs the maintenance menu for the application """
#     options:int = 3
#     while True:
#         print_banner("MAINTENANCE")
#         dynamic_fprint(maintenance_menu)
#         choice = get_menu_selection(options)
#
#         if choice == 1:
#             for tf in ["15", "60", "240", "D", "W"]:
#                 dbm = DatabaseManager("BTCUSDT", tf) 
#                 dbm.update_table()
#                 dbm.export_csv()
#             input("\n>> Hit enter to continue")
#         elif choice == 2:
#             # Combined with whats in the agent class, this should move to a 
#             # retraining class that can simply be called from here, and which 
#             # calls whichever algos/model building it needs from within the class.
#             agent = Engine()
#             mod = agent.list_models("./models")
#             agent.print_models(mod)
#
#             if len(mod) == 0:
#                 print("\nThere are no models to retrain, go create one... blah blah.")
#                 return;
#
#             print("\nWhich model would you like to retrain\n")
#             model = get_menu_selection(len(mod)+1)
#             if model == len(mod)+1:
#                 break
#
#             choosen_model = mod[model-1]['name']
#             a = choosen_model.split("-")[0]
#             t = choosen_model.split("-")[1]
#             agent = Engine(a, t)
#             agent.retrain(f"./models/{a}-{t}-model.pth")
#
#             input("\n>> Hit enter to continue")
#         else:
#             return;
#
#
