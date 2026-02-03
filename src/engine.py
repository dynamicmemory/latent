""" 
This class should be an orchestration class that brings everything together 
"""
from pandas.core.frame import is_1d_only_ea_dtype
from src.miniML.machLearnTools import MachLearnTools
from src.exchange import Exchange
from src.databaseManager import DatabaseManager
from src.features import Features 
from src.torchnn import Torchnn
from src.strategy import Strategy
from src.tradeManager import TradeManager
from datetime import datetime
import os 
import time
import threading 

TIME_MAP: dict[str, int] = {
    "15": 900000,
    "60": 3600000,
    "240": 14400000,
    "D": 86400000,
    "W": 604800000
}

class Engine:
    def __init__(self, asset:str="BTCUSDT", timeframe:str="15"):
        self.asset = asset
        self.timeframe = timeframe
        self.dbm = None
        self.features = None
        self.mlt = None
        self.torchnn = None
        self.trade = TradeManager(self.asset, self.timeframe)
        self.stop_event = threading.Event()
        self.thread = None
        

    def start_automation(self):
        """Starts automation in a separate thread."""
        if self.thread and self.thread.is_alive():
            print("Automation already running")
            return

        self.stop_event.clear()

        self.thread = threading.Thread(target=self._automation_loop, daemon=True)
        self.thread.start()
        print("Automation thread started")
        return 


    def _automation_loop(self):
        """Runs continuously while self.running=True."""
        # UTC milliseconds / 1000 = seconds = 1 time frame
        interval = TIME_MAP[self.timeframe] / 1000 

        while not self.stop_event.is_set():
            try:
                self.market_cycle()
                print("\nHit enter to continue\n>> ", end="")
            except Exception as e:
                print(f"Error in automation cycle: {e}")

            self.stop_event.wait(interval)


    # TODO: Check for open position and orders and auto close out and cancel all?
    def stop_automation(self):
        """Stops the automation loop."""
        if not self.thread or not self.thread.is_alive():
            print("Automation was not running.")       
            return 

        self.trade.cancel_orders_close_position()
        self.stop_event.set()
        self.thread.join()
        print("Automation stopped")       


    def get_model(self, X_train, X_test, y_train, y_test) :
        model_path:str = f"./models/{self.asset}-{self.timeframe}-model.pth"
        # Train a model if one doesnt exist otherwise load model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        if os.path.exists(model_path):
            print("Loading pretrained model")
            self.torchnn = Torchnn(self.mlt, X_train, X_test, y_train, y_test)
            self.torchnn.load_checkpoint(model_path)
        else:
            print(f"Training new model on {self.asset} - {self.timeframe}") 
            self.torchnn = Torchnn(self.mlt, X_train, X_test, y_train, y_test, training=True)
            self.torchnn.save_checkpoint(model_path)


    # The way the torchnn is currently built, we must always pass in x, y 
    # test and train set (this will change in future update) therefore we 
    # must go through the process of feature engineering and spliting the 
    # data sets to obtain an instance of the network to call predict on...
    def market_cycle(self) -> None:
        """Runs full pipeline of the trading engine"""
        # ensure the database is up to date 
        self.dbm = DatabaseManager(self.asset, self.timeframe)
        self.dbm.update_table()


        self.features = Features(self.dbm.get_dataframe())
        X, y = self.features.run_features()

        # Prep data for the model
        self.mlt = MachLearnTools(X, y)
        X_train, X_test, y_train, y_test = self.mlt.timeseries_pipeline()

        # load the model into memory and make a prediction
        self.get_model(X_train, X_test, y_train, y_test)
        decision:int = self.torchnn.predict()
        # Hard coded for on the fly debugging and testing
        # decision = 1

        # Find current market risk level
        self.strategy = Strategy(X)
        risk: str = self.strategy.main()

        self.trade.manage_trade(decision, risk)
        return 


    def test(self):
        e = Exchange(self.asset, self.timeframe)
        print(e.get_price())


    def manual_prediction(self, model_path:str):
        # Get data
        self.dbm = DatabaseManager(self.asset, self.timeframe)

        # Engineer features
        self.features = Features(self.dbm.get_dataframe())
        X, y = self.features.run_features()

        # Prep data for the model
        self.mlt = MachLearnTools(X, y)
        X_train, X_test, y_train, y_test = self.mlt.timeseries_pipeline()

        # Train a model if one doesnt exist otherwise load model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        if os.path.exists(model_path):
            print("Loading pretrained model")
            self.torchnn = Torchnn(self.mlt, X_train, X_test, y_train, y_test)
            self.torchnn.load_checkpoint(model_path)
        else:
            print(f"Training new model on {self.asset} - {self.timeframe}") 
            self.torchnn = Torchnn(self.mlt, X_train, X_test, y_train, y_test, training=True)
            self.torchnn.save_checkpoint(model_path)

        # Eval and predict
        self.torchnn.evaluation()
        decision = self.torchnn.predict()

        self.strategy = Strategy(X)
        curr_mkt_risk: str = self.strategy.main()


###################### Retraining and printing out models ####################
    ## Needs to move to its own class, but also need the algos for Retraining
    ## Maybe own class that calls this or whichever class eventually holds algos


    def list_models(self, model_path: str) -> list:
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


    # Probably doesnt belong here and should move to the menu
    def print_models(self, models:list) -> None:
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
        

    def retrain(self, model_path):
        """
        Retrains a model 

            Args:
                model_path - File path to save the newly trained model too, 
                             made up from the asset name and timeframe.
        """
        # Get data
        self.dbm = DatabaseManager(self.asset, self.timeframe)

        # Engineer features
        self.features = Features(self.dbm.get_dataframe())
        X, y = self.features.run_features()

        # Prep data for the model
        self.mlt = MachLearnTools(X, y)
        X_train, X_test, y_train, y_test = self.mlt.timeseries_pipeline()

        print(f"Retraining model {self.asset} - {self.timeframe}") 

        # Retrain the model and save it to the provided path
        self.torchnn = Torchnn(self.mlt, X_train, X_test, y_train, y_test, training=True)
        self.torchnn.save_checkpoint(model_path)

        print(f"\nModel has been retrained successfull.\n")
