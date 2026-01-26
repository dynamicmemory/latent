""" 
This class should be an orchestration class that brings everything together 
"""
from src.miniML.machLearnTools import MachLearnTools
from src.exchange import Exchange
from src.databaseManager import DatabaseManager
from src.features import Features 
from src.torchnn import Torchnn
from src.strategy import Strategy
from src.riskCalculator import RiskCalculator
from src.accountManager import AccountManager
from src.apiManager import api_key, api_secret

import os
from datetime import datetime
# Hard coded for testing, will be passed in or initiated via user.
asset = "BTCUSDT"
timeframe = "15"

class Engine:
    def __init__(self, asset:str="BTCUSDT", timeframe:str="15"):
        self.asset = asset
        self.timeframe = timeframe
        self.dbm = None
        self.features = None
        self.mlt = None
        self.torchnn = None
        self.strategy = None


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


    def start_automation(self) -> None:
        """Runs full pipeline of the trading engine"""
        # ensure the database is up to date 
        self.dbm = DatabaseManager(self.asset, self.timeframe)
        self.dbm.update_table()

        # The way the torchnn is currently built, we must always pass in x, y 
        # test and train set (this will change in future update) therefore we 
        # must go through the process of feature engineering and spliting the 
        # data sets to obtain an instance of the network to call predict on...
        self.features = Features(self.dbm.get_dataframe())
        X, y = self.features.run_features()

        # Prep data for the model
        self.mlt = MachLearnTools(X, y)
        X_train, X_test, y_train, y_test = self.mlt.timeseries_pipeline()

        # load the model into memory and make a prediction
        self.get_model(X_train, X_test, y_train, y_test)
        decision:int = self.torchnn.predict()

        # Find current market risk level
        self.strategy = Strategy(X)
        curr_mkt_risk: str = self.strategy.main()

        account = AccountManager(api_key, api_secret, True)
        ctrade, csize = account.get_position("linear", self.asset)
        # No trade predicted
        if decision == 2:
            return
            print("There is currently no trade to make.")
        # Predicted trade matches current position
        elif decision == ctrade:
            print("Current trade matches current position")
            return 
        elif decision != ctrade:
            # close current trade, calculate & open new trade
            self.trade_manager(account, ctrade, csize ,decision, curr_mkt_risk) 
            print("Trade manager loop")
            return
        else:
            print("Unknown error for now")
            return

        

    # Soon to be its own class I think
    def trade_manager(self, account, ctrade:int, csize:float, pred:int, risk):
        # Cancel all stops and limit orders
        account.cancel_all_USDT_orders("linear")
        if ctrade == 2:
            # Place new order 
            return 
        else:
            # close current trade 
            account.create_market_order(self.asset, pred, csize)            
            # calc new order 

            # This all has to be atomic, all work or none happen.
            # place it 

            # place take profit

            # place stop 

            return



    def stop_automation(self) -> None:
        """Gracefully enters the automation cycling"""
        pass


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

        # For the time being, this is the equiv of executing a market order
        self.get_trade_details(self.asset, self.timeframe, curr_mkt_risk, decision)




    # Specifically only for manual predictions
    def get_trade_details(self, asset, timeframe, risk, direction):
        self.exchange = Exchange(asset, timeframe)
        # Hardcoding for time being
        entry: float = int(float(self.exchange.get_ohlc()[-1][1]))
        # Hard coded arbitrary stop for the time being 
        stop, target = 0, 0
        if direction == 1:
            stop: int = int(float(self.exchange.get_ohlc()[-2][3]))
            target: int = (entry - stop) * 2 + entry
        elif direction == 0: 
            stop: int = int(float(self.exchange.get_ohlc()[-2][2]))
            target: int = entry - (stop - entry) * 2
        else:
            # no trade decision, tell users
            print(f"Agent doesn't see a good trade currently")
            return

        rc = RiskCalculator()
        size, risk_percentage = rc.main(entry, stop, risk)

        # Printing info instead of sending to the exchange to execute trade 
        print(asset)
        print(f"Time Frame:\t{timeframe}")
        print(f"Risk Level:\t{risk}")
        print(f"Direction:\t{direction}")
        print(f"Entry Level:\t${entry}")
        print(f"Stop Level:\t${stop}")
        print(f"Target pri:\t${target}")
        print(f"Size of Pos:\t${size}")


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
