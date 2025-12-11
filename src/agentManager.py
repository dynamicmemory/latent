# TODO: Build strategy class 
# TODO: Build riskmanagement class
# TODO: Rebuild DatabaseManager (brittly at first, circle back once db rebuild)
# TODO: Rebuild NN to ANN 
# TODO: Build CNN 
# TODO: Auth Exchange, Build trade apis
# TODO: Rebuild Database
# TODO: Build Simulator
# TODO: Build logger
# TODO: Build CLI command client
# TODO: Async the whole thing
# TODO: put it on the server to live

from src.miniML.models.neuralNetwork import NeuralNetwork 
from src.miniML.machLearnTools import MachLearnTools
from src.exchange import Exchange
from src.databaseManager import DatabaseManager
from src.features import Features 
from src.strategy import Strategy
import numpy as np


class Agent:
    # Build an init
    def main(self):
        time_list: list = ["15", "60", "240", "D", "W"] # Add daily back in once tests done
        asset = "BTCUSDT"
        # self.update_all_tf(asset, time_list)
        timeframe = "15"

        fname: str = f"{asset}-{timeframe}.csv"
        ex = Exchange(asset, timeframe)
        dbm = DatabaseManager(fname, timeframe,ex)

        f = Features(dbm.get_data())
        X, y = f.run_features()
        mlt = MachLearnTools(X, y)
        X_train, X_test, y_train, y_test = mlt.timeseries_pipeline()

        layers = [[8, "relu"], [8, "relu"]]
        model = NeuralNetwork(X_train, y_train, "binary", epochs = 10000, lr=0.02, layers=layers)
        model.fit()
        
        x_pred = mlt.latest_features()
        
        # TODO: MOVE INTO WHEREEVER IM DOING THIS... MLT I THINK
        x_pred = np.resize(x_pred, (1, model.X.shape[1]))  # force shape match if tiny diff
        
        pred_val = model.predict(x_pred)
        print("Buy" if pred_val > 0.5 else "sell")

        strat = Strategy(X)
        strat.main()
        # Run sentiment analysis to get an idea on which strategy to select 

        # Main 
        # Agentmanager 
        # Queries exchange 
        # Updates database 
        # Feeds raw values into features 
        # calculates features 
        # miniML transform data for training 
        # strategy calculates risk level, dictates: tf, asset, risk%, stopwidth, etc
        # trains network
        # makes prediction
        # executes order on exchange
        # goes idle waiting for next tf update.
        # starts again.


    def update_all_tf(self, asset:str, time_list:list) -> None:
        # Updates all timeframes databases, probably move this to another class 

        for time in time_list: 
            fname: str = f"{asset}-{time}.csv"
            ex = Exchange(asset, time)
            dbm = DatabaseManager(fname, time, ex)
            dbm.update_db()
            print(f"{time} data updated")

