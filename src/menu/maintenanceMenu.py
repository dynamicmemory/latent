from src.engine import Engine
from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings
from src.databaseManager import DatabaseManager

class MaintenanceMenu(IMenu):
    def __init__(self, settings: Settings, engine: Engine):
        self.settings = settings
        self.engine = engine
        self.menu: dict[int, list] = {
            1: ["Update Database", self.update_database],
            2: ["Retrain Models", self.retrain_models],
        }


    def run(self) -> None:
        menu_runner(title, self.menu, header, lambda: [])


    def update_database(self) -> None:
        for key, timeframe in TIME_MAP.items():
            if key == 0:
                continue

            dbm = DatabaseManager(asset_tostring(self.settings.asset()), 
                                  timeframe) 
            dbm.update_table()
            dbm.export_csv()


    # Retraining models should not belong with the engine, there should be a 
    # model class of some kind or model manager, which should contain retrain 
    # that is callable from this menu
    def retrain_models(self) -> None:
        models = self.engine.list_models("./pickled_models")
        self.engine.print_models(models)

        if len(models) == 0:
            print("\nThere are no models to retrain, go create one... blah blah.")
            return;

        print("\nWhich model would you like to retrain\n")
        model = get_menu_selection(len(models)+1)
        if model == len(models)+1:
            return 

        choosen_model = models[model-1]['name']
        a = choosen_model.split("-")[0]
        t = choosen_model.split("-")[1]
        self.engine.retrain(f"./pickled_models/{a}-{t}-model.pth", a, t)


title: str = "Maintenance"
header: str = "Maintenance Menu"
