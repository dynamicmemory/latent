
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


# TODO: Clean this up by moving every task to their rightful place please!!!
def main():
    update_all_tf()

    # Still hard coding Daily while building 
    timeframe = "D"
    fname: str = f"{bitcoin}-{timeframe}.csv"
    ex = exchange(bitcoin, timeframe)
    dbm = databaseManager(fname, timeframe,ex)
    # dbm.update_db()

    # Engineer the features
    f = features(fname)
    X_train, X_test, y_train, y_test = f.build_data()
    # print(X_train.shape, y_train.shape)
    # print(X_test.shape, y_test.shape)

    # CREATE CLASS FOR BUILDING NN ARCHITECTURE AND DEPLOYING
    # Build the NN and feed it the features
    layers = [[4, "relu"], [8, "relu"]]
    model = nn(X_train, y_train, "binary", epochs = 1000, lr=0.02, layers=layers)
    model.fit()

    x_pred = f.latest_features()
    x_pred = np.resize(x_pred, (1, model.X.shape[1]))  # force shape match if tiny diff
    pred_val = model.predict(x_pred)
    print("Buy" if pred_val > 0.5 else "sell")


if __name__ == "__main__":
    main()


# Phase 2 
# Exchange Auth 
# Manual and auto ability to set and cancel trades 
# Logging of entire system 
# Dashboard viewing integration

# Phase 3 
# End to End mode 
# Rebuild DB in SQLite
# Consider different model architectures 

# main()
  # Enter asset + tf 
  # Creates exchange
  # Creates db passing in asset + tf + exchange 
    # db updates with latest data from exchange 

  # Train/Retrain network on new data, save new model? 
    # Calculate features 
    # Select model architecture 
    # Load pretrained model?
    # New cycle of training?
 
  # Decide on action to take 
    # Check positions?
    # Change Strategy?
    # Simulate the market?
    # Run the model i.e vibe-trading?
    # Force open/close position i.e self-trading?
    # Automate?
    # Exit?

  # Lets choose automate at the moment as that runs the end to end features 
  
  # Automate 
    # ....
