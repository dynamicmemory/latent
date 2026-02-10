
""" 
This class should be an orchestration class that brings everything together 
"""
from src.account.accountManager import AccountManager
from src.data.dataManager import DataManager
from src.account.strategy import Strategy
from src.account.tradeManager import TradeManager
from src.models.modelManager import ModelManager
from src.engine.automationEngine import AutomationEngine
import os
import threading 

class Engine:
    def __init__(self, account: AccountManager, data: DataManager, settings: Settings):
        self.asset = settings.asset()
        self.timeframe = settings.timeframe()
        self.settings = settings
        self.account_manager = account
        self.data = data
        self.model = None # OPTIONAL load a model from the saved asset and timeframe settings?
        self.automating = False
        self.autoEngine = None


    def start_automation(self) -> None:
        """Starts the automation loop."""
        if not self.automating:
            self.autoEngine = AutomationEngine(self.settings, self.account_manager)
            self.autoEngine.start_automation()
            self.automating = True 
        else:
            print("Already running the automation engine")
        return 


    def stop_automation(self) -> None:
        """Stops the automation loop."""
        if self.automating:
            self.autoEngine.stop_automation()
            self.automating = False 
        else:
            print("The automation engine isn't running")
        return


    def manual_prediction(self, asset:str, timeframe:str):
        """Makes a prediction using on the passed in asset and timeframe. """
        X_train, y_train = self.data.get_training_set()
        X_test, y_test = self.data.get_testing_set()
        X_latest = self.data.get_latest()

        self._get_model(X_train, y_train, asset, timeframe)
        # self.model.evaluation(X_test, y_test)
        decision = self.model.predict(X_latest, X_train)

        print("Models predicts: ", end="")
        print("Buy" if decision == 1 else "Sell" if decision == 0 else "No trade")


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
