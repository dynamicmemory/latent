from src.exchange import Exchange as exchange
from src.databaseManager import DatabaseManager as databaseManager 
from src.features import Features as features
from src.neuralnetwork import NN as nn 
import numpy as np

base: str = "https://api.bybit.com"
tickers: str = "/v5/market/tickers"
kline: str = "/v5/market/kline"
timeframe: str = "D"
bitcoin: str = "BTCUSDT"
time_list: list = ["15", "60", "240", "D", "W"] # Add daily back in once tests done

def update_all_tf():
    # Updates all timeframes databases, probably move this to another class 
    for time in time_list: 
        fname: str = f"{bitcoin}-{time}.csv"
        ex = exchange(bitcoin, time)
        dbm = databaseManager(fname, time, ex)
        dbm.update_db()
        print(f"{time} data updated")

def main():
    update_all_tf()

    # Still hard coding Daily while building 
    timeframe = "15"
    fname: str = f"{bitcoin}-{timeframe}.csv"
    ex = exchange(bitcoin, timeframe)
    dbm = databaseManager(fname, timeframe,ex)
    # dbm.update_db()

    # Engineer the features
    f = features(fname)
    X_train, X_test, y_train, y_test = f.build_data()
    # print(X_train.shape, y_train.shape)
    # print(X_test.shape, y_test.shape)

    # Build the NN and feed it the features
    layers = [[4, "relu"], [3, "relu"]]
    model = nn(X_train, y_train, "binary", epochs = 1000, lr=0.01, layers=layers)
    model.fit()

    x_pred = f.latest_features()
    x_pred = np.resize(x_pred, (1, model.X.shape[1]))  # force shape match if tiny diff
    pred_val = model.predict(x_pred)
    print("Buy" if pred_val > 0.5 else "sell")


if __name__ == "__main__":
    main()


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


# class features 
# class feature_manager
    # class calculate_features
    # class prepare_features
    

