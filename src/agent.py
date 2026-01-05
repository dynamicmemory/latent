""" 
This class should be an orchestration class that brings everything together 
"""
from src.miniML.machLearnTools import MachLearnTools
from src.exchange import Exchange
from src.sqlitedb import DatabaseManager
from src.features import Features 
from src.torchnn import Torchnn
from src.strategy import Strategy
from src.riskCalculator import RiskCalculator

# Hard coded for testing, will be passed in or initiated via user.
asset = "BTCUSDT"
timeframe = "15"

class Agent:
    def __init__(self, asset:str="BTCUSDT", timeframe:str="15"):
        self.asset = asset
        self.timeframe = timeframe
        self.dbm = None
        self.features = None
        self.mlt = None
        self.torchnn = None
        self.strategy = None
        # auto running for testing purposes
        self.run_agent()
        # self.run_all_tf()

    def test(self):
        e = Exchange(self.asset, self.timeframe)
        print(e.get_price())


    def run_agent(self):
        print(f"Training on {self.asset} - {self.timeframe}") 
        # Get data
        self.dbm = DatabaseManager(self.asset, self.timeframe)

        # Engineer features
        self.features = Features(self.dbm.get_dataframe())
        X, y = self.features.run_features()

        # Prep data for the model
        self.mlt = MachLearnTools(X, y)
        X_train, X_test, y_train, y_test = self.mlt.timeseries_pipeline()

        # Auto train the model
        self.torchnn = Torchnn(self.mlt, X_train, X_test, y_train, y_test)

        # Eval and predict
        self.torchnn.evaluation()
        decision = self.torchnn.predict()

        self.strategy = Strategy(X)
        curr_mkt_risk: str = self.strategy.main()

        # For the time being, this is the equiv of executing a market order
        self.get_trade_details(self.asset, self.timeframe, curr_mkt_risk, decision)


    # Testing purposes only
    def run_all_tf(self):
        time_list: list = ["15", "60", "240", "D", "W"] 
        for timeframe in time_list:
            window = 30
            self.dbm = DatabaseManager(asset, timeframe)
            self.features = Features(self.dbm.get_dataframe())
            X, y = self.features.run_features()
            self.mlt = MachLearnTools(X, y)
            X_train, X_test, y_train, y_test = self.mlt.timeseries_pipeline(window)
            self.torchnn = Torchnn(self.mlt, X_train, X_test, y_train, y_test, window=window)
            self.torchnn.evaluation()
            self.torchnn.predict()


    # We dont need to pass asset and tf now, we can just use self.
    # We would execute a trade instead of all these calcs just to print it.
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
