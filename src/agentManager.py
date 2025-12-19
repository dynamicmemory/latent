from src.miniML.models.neuralNetwork import NeuralNetwork 
from src.miniML.machLearnTools import MachLearnTools
from src.exchange import Exchange
from src.databaseManager import DatabaseManager
from src.features import Features 
from src.strategy import Strategy
from src.riskCalculator import RiskCalculator
import numpy as np


class Agent:
    def __init__(self):
        self.exchange = None
        self.dbm = None
        self.features = None
        self.miniML = None
        self.model = None
        self.strategy = None
        self.riskcalculator = None
        self.setup_agent()


    def setup_agent(self):
        """ Idea is you create the agent in main and then get all the input 
            here either from the user or hahncoded and then setup all the 
            objects/classes you need to manager the trading flow 
        """
        time_list: list = ["15", "60", "240", "D", "W"] 
        asset: str = "BTCUSDT"
        timeframe: str = "0"
        fname: str = f"{asset}-{timeframe}.csv"

        self.exchange = Exchange(asset, timeframe)
        self.dbm = DatabaseManager(fname, timeframe, self.exchange)
        self.features = Features(self.dbm.get_data())
        X, y = self.features.run_features()
        self.miniML = MachLearnTools(X, y)


    # Build an init
    def main(self):
        time_list: list = ["15", "60", "240", "D", "W"] 
        asset = "BTCUSDT"
        self.update_all_tf(asset, time_list)
        self.new_zeff_flow()


    def new_zeff_flow(self):
        # Creating lists of all the info we want
        time_list: list = ["15", "60", "240", "D", "W"]
        risk_list: list = []
        dir_list: list = []
        entry_list: list = []
        stop_list: list = []
        target_list: list = []
        size_list: list = []

        asset = "BTCUSDT"

        for timeframe in time_list:
            # Running model flow and getting prediction
            fname: str = f"{asset}-{timeframe}.csv"
            ex = Exchange(asset, timeframe)
            dbm = DatabaseManager(fname, timeframe,ex)

            f = Features(dbm.get_data())
            X, y = f.run_features()
            mlt = MachLearnTools(X, y)
            X_train, X_test, y_train, y_test = mlt.timeseries_pipeline()

            # Looks like NN needs a manager or something 
            layers = [[8, "relu"], [8, "relu"]]
            model = NeuralNetwork(X_train, y_train, "binary", epochs = 1000, lr=0.02, layers=layers)
            model.fit()
        
            x_pred = mlt.latest_features()
            x_pred = np.resize(x_pred, (1, model.X.shape[1]))  # force shape match if tiny diff
        
            pred_val = model.predict(x_pred)
            direction = "Buy" if pred_val > 0.5 else "Sell"

            # Using clustering to find the risk we will choose aka strategy
            strat = Strategy(X)
            risk = strat.main()
            risk_list.append(risk)
            dir_list.append(direction)

            # Hardcoding for time being
            entry: float = int(float(ex.get_ohlc()[-1][1]))
            entry_list.append(entry)

            # Hard coded arbitrary stop for the time being 
            stop, target = 0, 0
            if direction == "Buy":
                stop: int = int(float(ex.get_ohlc()[-2][3]))
                target: int = (entry - stop) * 2 + entry
            else: 
                stop: int = int(float(ex.get_ohlc()[-2][2]))
                target: int = entry - (stop - entry) * 2
            stop_list.append(stop)
            target_list.append(target)

            # print(ex.get_ohlc()[-1])
                
            c = RiskCalculator()
            size, risk_percentage = c.main(entry, stop, risk)
            size_list.append(size)

        # Printing info instead of automating trade currently
        print(asset)
        print("Time Frame\t", end="")
        for t in time_list:
            print(f"{t}\t", end="")
        print("\nRisk Level\t", end="")
        for r in risk_list:
            print(f"{r}\t", end="")
        print("\nDirection\t", end="")
        for d in dir_list:
            print(f"{d}\t", end="")
        print("\nEntry Level\t", end="")
        for e in entry_list:
            print(f"${e:,}\t", end="")
        print("\nStop Level\t", end="")
        for s in stop_list:
            print(f"${s:,}\t", end="")
        print("\nTarget pri\t", end="")
        for t in target_list:
            print(f"${t:,}\t", end="")
        print("\nSize of Pos\t", end="")
        for p in size_list:
            print(f"${p:,} ", end="")
        print("\n")


    def update_all_tf(self, asset:str, time_list:list) -> None:
        # Updates all timeframes databases, probably move this to another class 

        for time in time_list: 
            fname: str = f"{asset}-{time}.csv"
            ex = Exchange(asset, time)
            dbm = DatabaseManager(fname, time, ex)
            dbm.update_db()
            print(f"{time} data updated")


    # one market update cycle (trade)
    def tick(self):
        pass

    def update_position(self):
        pass 

    def train_model(self):
        pass 

    def log_metrics(self):
        pass


    def get_risk(self):





