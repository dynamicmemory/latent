import os 
from datetime import datetime
from src.engine.engine import Engine
from src.menus.menuInterface import IMenu
from src.menus.menuUtilities import *
from src.settings.settings import Settings
from src.data.databaseManager import DatabaseManager

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

            dbm = DatabaseManager(self.settings.asset(), timeframe) 
            dbm.update_table()
            print(f"Updating {self.settings.asset()}-{timeframe}")
            dbm.export_csv()
            print(f"Exporting update to backup csv")

        input("\nHit enter to continue")


    # Retraining models should not belong with the engine, there should be a 
    # model class of some kind or model manager, which should contain retrain 
    # that is callable from this menu
    def retrain_models(self) -> None:
        models = self._list_models("./pickled_models")
        self._print_models(models)

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
        input("\nHit enter to continue")


    def _list_models(self, model_path: str) -> list:
        """
        Searches the provided DIR for all models saved

        Args:
            model_path - location of saved modesl
        """
        models = []

        if not os.path.exists(model_path):
            return models 

        for fname in os.listdir(model_path):
            if not fname.endswith(".pth"):
                continue 

            path = os.path.join(model_path, fname)
            mtime = os.path.getmtime(path)
            last_modified = datetime.fromtimestamp(mtime)

            models.append({
                "name": fname,
                "path": path, 
                "last_modified": last_modified,
            })

        models.sort(key=lambda x: x["last_modified"], reverse=True)
        return models


    def _print_models(self, models:list) -> None:
        """
        Prints out the name, and last modified date for all models provided.

        Args: 
            models - a list containing all saved models in a directory.
        """
        if not models:
            print("No models found.")
            return 

        i:int = 1
        for m in models:
            print(f"{i}. {m['name']:<22} - "
                  f"Last updated: {m['last_modified'].strftime('%Y-%m-%d %H:%M:%S')}")
            i +=1
        print(f"{i}. Return to maintenance menu.\n")


title: str = "Maintenance"
header: str = "Maintenance Menu"
