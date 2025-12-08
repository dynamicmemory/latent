import sys
from src.exchange import Exchange as exchange
from src.databaseManager import DatabaseManager as databaseManager 
from src.agentManager import Agent

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
    # update_all_tf()

    # Still hard coding Daily while building 
    timeframe = "15"
    fname: str = f"{bitcoin}-{timeframe}.csv"
    ex = exchange(bitcoin, timeframe)
    dbm = databaseManager(fname, timeframe,ex)
    # Passing dbm into agent for now but this is incorrect
    agent = Agent()
    agent.main(dbm)

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
