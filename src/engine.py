""" 
This class should be an orchestration class that brings everything together 
"""
from src.accountManager import AccountManager
from src.data.dataManager import DataManager
from src.strategy import Strategy
from src.tradeManager import TradeManager
from src.models.modelManager import ModelManager
import os
import threading 

TIME_MAP: dict[str, int] = {
    "15": 900000,
    "60": 3600000,
    "240": 14400000,
    "D": 86400000,
    "W": 604800000
}

# INITIALIZE asset and timeframe via settings
class Engine:
    def __init__(self, account: AccountManager, data: DataManager, asset:str="BTCUSDT", timeframe:str="15"):
        self.asset = asset
        self.timeframe = timeframe
        self.account_manager = account
        self.data = data

        self.model = None # OPTIONAL load a model from the saved asset and timeframe settings?

        # Needs to load from settings, stale state occurs.
        self.trade = TradeManager(self.account_manager, self.asset, self.timeframe)
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


    def market_cycle(self) -> None:
        """Runs full pipeline of the trading engine"""
        X_train, y_train = self.data.get_training_set()
        X_latest = self.data.get_latest()
        X_features = self.data.get_X_features()

        # load the model into memory and make a prediction
        self._get_model(X_train, y_train, self.asset, self.timeframe)
        decision:int = self.model.predict(X_latest, X_train)
        self.strategy = Strategy(X_features)
        risk: str = self.strategy.main()
        self.trade.manage_trade(decision, risk)
        print("Market cycle finished")
        return 


    def manual_prediction(self, model_path:str, asset:str, timeframe:str):
        X_train, y_train = self.data.get_training_set()
        X_test, y_test = self.data.get_testing_set()
        X_latest = self.data.get_latest()

        self._get_model(X_train, y_train, asset, timeframe)
        self.model.evaluation(X_test, y_test)
        decision = self.model.predict(X_latest)
        print(decision)


    def _get_model(self, X_train, y_train, asset, timeframe):
        model_path:str = f"./pickled_models/{asset}-{timeframe}-model.pth"

        # Train a model if one doesnt exist otherwise load model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        if os.path.exists(model_path):
            print("Loading pretrained model")
            self.model = ModelManager()
            self.model.select("lstm") 
            self.model.load(model_path)
        else:
            print(f"Training new model on {asset} - {timeframe}") 
            self.model = ModelManager()
            self.model.select("lstm") 
            self.model.train(X_train, y_train)
            self.model.save(model_path)


    def retrain(self, model_path, asset, timeframe):
        """
        Retrains a model 

            Args:
                model_path - File path to save the newly trained model too, 
                             made up from the asset name and timeframe.
        """
        X_train, y_train = self.data.get_training_set()

        print(f"Retraining model {asset} - {timeframe}") 
        self.model = ModelManager()
        self.model.select("lstm") 
        self.model.train(X_train, y_train)
        self.model.save(model_path)

        print(f"\nModel has been retrained successfull.\n")
