from src.data.dataManager import DataManager
from src.account.strategy import Strategy
from src.account.tradeManager import TradeManager
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

class AutomationEngine: 
    def __init__(self, settings, account_manager) -> None:
        self.asset = settings.asset()
        self.timeframe = settings.timeframe()
        self.account_manager = account_manager
        self.data_manager = DataManager(self.asset, self.timeframe) 
        self.trade = TradeManager(self.account_manager, self.asset, self.timeframe)
        self.stop_event = threading.Event()
        self.model = None
        self.thread = None


    def start_automation(self):
        """Starts automation in a separate thread."""
        if self.thread and self.thread.is_alive():
            print("Automation already running")
            return

        self.stop_event.clear()

        print("Automation thread started")
        self.market_cycle()

        self.thread = threading.Thread(target=self._automation_loop, daemon=True)
        self.thread.start()
        return 


    def _automation_loop(self):
        """Runs continuously while self.running=True."""
        # UTC milliseconds / 1000 = seconds = 1 time frame
        interval = TIME_MAP[self.timeframe] / 1000 
        self.stop_event.wait(interval)

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
        self.data_manager.update_data(self.asset, self.timeframe)
        X_train, y_train = self.data_manager.get_training_set()
        X_latest = self.data_manager.get_latest()
        X_features = self.data_manager.get_X_features()

        # load the model into memory and make a prediction
        if self.model is None:
            self._get_model(X_train, y_train, self.asset, self.timeframe)

        decision: float = self.model.predict(X_latest, X_train)
        self.strategy = Strategy(X_features)
        risk: str = self.strategy.main()
        self.trade.manage_trade(decision, risk)
        return 


    def _get_model(self, X_train, y_train, asset, timeframe):
        """ Loads a pretrained model if one exists, otherwise trains a new 
        model on the provided asset and timeframe using the X_training set."""
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


