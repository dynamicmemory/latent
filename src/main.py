from src.exchange import Exchange as exchange
from src.databaseManager import DatabaseManager as databaseManager 
from src.features import Features as features
from src.nn import NN as nn 
import numpy as np

base: str = "https://api.bybit.com"
tickers: str = "/v5/market/tickers"
kline: str = "/v5/market/kline"
timeframe: str = "D"
bitcoin: str = "BTCUSDT"
time_list: list = ["15", "60", "240", "W"] # Add daily back in once tests done

def main():
    # Updates all timeframes databases, probably move this to another class 
    # for time in time_list: 
    #     fname: str = f"{bitcoin}-{time}.csv"
    #     ex = exchange(bitcoin, time)
    #     dbm = databaseManager(fname, time, ex)
    #     dbm.update_db()
    #     print(f"{time} data updated")

    # Still hard coding Daily while building 
    fname: str = f"{bitcoin}-{timeframe}.csv"
    ex = exchange(bitcoin, timeframe)
    dbm = databaseManager(fname, timeframe,ex)
    dbm.update_db()

    f = features(fname)
    f.compute() 
    # NNmanager to 
        # Prep features for NN
        # build NN
        # Feed preped features into NN 
        # Return decision


if __name__ == "__main__":
    main()

    # ------- NN TESTING ---------
    # np.random.seed(1)
    #
    # X = np.random.rand(6, 3)
    # y = (np.random.rand(6, 1) > 0.5).astype(float)
    # layers = [[5, "relu"], [4, "relu"]]
    #
    # model = nn(X, y, "binary", epochs=1000, lr=0.01, layers=layers)
    # model.fit()

# Phase 1 
# Run Program
# Checks db for history and syncs up latest price records 
# Calculates features 
# Builds nn
# Comes to a market conclusion

# Phase 2 
# Exchange Auth 
# Manual and auto ability to set and cancel trades 
# Logging of entire system 
# Dashboard viewing integration

# Phase 3 
# End to End mode 
# Rebuild DB in SQLite
# Rebuild agent from NN to probabilistic 
