""" 
This class should be an orchestration class that brings everything together 
"""
from src.miniML.models.neuralNetwork import NeuralNetwork 
from src.miniML.machLearnTools import MachLearnTools
# from src.exchange import Exchange
from src.sqlitedb import DatabaseManager
from src.features import Features 
# from src.strategy import Strategy
# from src.riskCalculator import RiskCalculator
import numpy as np

asset = "BTCUSDT"
timeframe = "15"

class Agent:
    def __init__(self):
        self.dbm = None
        self.features = None
        self.new_clean_frfr_flow_this_time_i_promise(asset, timeframe)

    def new_clean_frfr_flow_this_time_i_promise(self, asset:str, timeframe:str):
        time_list: list = ["15", "60", "240", "D", "W"] 
        for timeframe in time_list:
            import torch
            import torch.nn as nn
            import torch.optim as optim
            from src.miniML.machLearnTools import MachLearnTools
            from src.features import Features
            from src.sqlitedb import DatabaseManager
            
            # --- Settings ---
            asset = "BTCUSDT"
            # timeframe = "15"
            window = 10
            epochs = 200
            lr = 0.001
            
            # --- Load data ---
            dbm = DatabaseManager(asset, timeframe)
            df = dbm.get_dataframe()
            
            features = Features(df)
            X, y = features.run_features()
            
            mlt = MachLearnTools(X, y)
            X_train, X_test, y_train, y_test = mlt.timeseries_pipeline(window=window)
            
            # --- Convert to PyTorch tensors ---
            X_train = torch.tensor(X_train, dtype=torch.float32)
            y_train = torch.tensor(y_train, dtype=torch.long)  # multi-class
            X_test = torch.tensor(X_test, dtype=torch.float32)
            y_test = torch.tensor(y_test, dtype=torch.long)
    
            # --- Define a simple time-series NN ---
            class TimeSeriesNN(nn.Module):
                def __init__(self, input_size, hidden_size=64, output_size=3):
                    super().__init__()
                    self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
                    self.fc = nn.Linear(hidden_size, output_size)
                
                def forward(self, x):
                    _, (h_n, _) = self.lstm(x)
                    out = self.fc(h_n[-1])
                    return out
            
            input_size = X_train.shape[2]  # features per timestep
            output_size = 3  # multi-class labels
            
            model = TimeSeriesNN(input_size, hidden_size=64, output_size=output_size)
            
            # --- Training setup ---
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters(), lr=lr)
            
            # --- Training loop ---
    
            y_train = torch.tensor(y_train.flatten(), dtype=torch.long)
            y_test = torch.tensor(y_test.flatten(), dtype=torch.long)
            for epoch in range(epochs):
                model.train()
                optimizer.zero_grad()
                outputs = model(X_train)
                loss = criterion(outputs, y_train)
                loss.backward()
                optimizer.step()
            
                if epoch % 20 == 0:
                    print(f"Epoch {epoch}: Loss = {loss.item():.4f}")
            
            # --- Evaluation ---
            model.eval()
            with torch.no_grad():
                preds = torch.argmax(model(X_test), dim=1)
                acc = (preds == y_test.flatten()).float().mean()
                print("Test Accuracy:", acc.item())
            
            # --- Predict next candle ---
            latest_X = torch.tensor(mlt.latest_features(window=window), dtype=torch.float32)
            latest_X = latest_X.reshape(1, window, X_train.shape[2])
            with torch.no_grad():
                pred_next = torch.argmax(model(latest_X), dim=1).item()
            print(f"Next candle prediction: {pred_next}")
            
    

    # def setup_agent(self):
    #     """ 
    #     Idea is you create the agent in main and then get all the input 
    #     here either from the user or hahncoded and then setup all the 
    #     objects/classes you need to manager the trading flow 
    #     """
    #     time_list: list = ["15", "60", "240", "D", "W"] 
    #     asset: str = "BTCUSDT"
    #     timeframe: str = "60"
    #     fname: str = f"{asset}-{timeframe}.csv"
    #
    #     self.dbm = DatabaseManager(asset, timeframe)
    #
    #     print(self.dbm.get_dataframe())
    #     self.features = Features(self.dbm.get_dataframe())
    #     X, y = self.features.run_features()
    #     self.miniML = MachLearnTools(X, y)
    #
    #     self.train_model()
    #     direction = self.get_prediction()
    #
    #     # TODO: Seems horrid to have to give this the dataframe from exchange
    #     self.strategy = Strategy(X)
    #     risk_level: str = self.strategy.main()
    #     self.riskcalculator = RiskCalculator()
    #     self.get_trade_details(asset, timeframe, risk_level, direction)
    #
    # def main(self):
    #     # self.update_all_tf()
    #     pass 

   
    # def update_all_tf(self) -> None:
    #     # Updates all timeframes databases, probably move this to another class 
    #     time_list: list = ["15", "60", "240", "D", "W"] 
    #     asset = "BTCUSDT"
    #
    #     for time in time_list: 
    #         fname: str = f"{asset}-{time}.csv"
    #         ex = Exchange(asset, time)
    #         dbm = DatabaseManager(fname, time, ex)
    #         dbm.update_db()
    #         print(f"{time} data updated")


    # TODO: Agent should not be doing this, move to miniML or modelManager 
    def train_model(self):
        X_train, X_test, y_train, y_test = self.miniML.timeseries_pipeline()

        layers = [[8, "relu"], [8, "relu"]]
        self.model = NeuralNetwork(X_train, y_train, "binary", epochs = 1000, lr=0.02, layers=layers)
        self.model.fit()
     

    # TODO: Move this to miniML->predictor class
    def get_prediction(self) -> str:
        x_pred = self.miniML.latest_features()
        x_pred = np.resize(x_pred, (1, self.model.X.shape[1]))  # force shape match if tiny diff
        
        pred_val = self.model.predict(x_pred)
        direction = "Buy" if pred_val > 0.5 else "Sell"
        return direction


    # def get_trade_details(self, asset, timeframe, risk, direction):
    #     self.exchange = Exchange(asset, timeframe)
    #     # Hardcoding for time being
    #     entry: float = int(float(self.exchange.get_ohlc()[-1][1]))
    #     # Hard coded arbitrary stop for the time being 
    #     stop, target = 0, 0
    #     if direction == "Buy":
    #         stop: int = int(float(self.exchange.get_ohlc()[-2][3]))
    #         target: int = (entry - stop) * 2 + entry
    #     else: 
    #         stop: int = int(float(self.exchange.get_ohlc()[-2][2]))
    #         target: int = entry - (stop - entry) * 2
    #
    #     size, risk_percentage = self.riskcalculator.main(entry, stop, risk)
    #
    #     # Printing info instead of sending to the exchange to execute trade 
    #     print(asset)
    #     print(f"Time Frame:\t{timeframe}")
    #     print(f"Risk Level:\t{risk}")
    #     print(f"Direction:\t{direction}")
    #     print(f"Entry Level:\t${entry}")
    #     print(f"Stop Level:\t${stop}")
    #     print(f"Target pri:\t${target}")
    #     print(f"Size of Pos:\t${size}")
    #
    #
    # def update_position(self):
    #     pass 
    #
    #
    # def log_metrics(self):
    #     pass
    #

    # def print_all_timeframe_stats(self):
    #     # Creating lists of all the info we want
    #     time_list: list = ["15", "60", "240", "D", "W"]
    #     risk_list: list = []
    #     dir_list: list = []
    #     entry_list: list = []
    #     stop_list: list = []
    #     target_list: list = []
    #     size_list: list = []
    #
    #     asset = "BTCUSDT"
    #
    #     for timeframe in time_list:
    #         # Running model flow and getting prediction
    #         fname: str = f"{asset}-{timeframe}.csv"
    #         ex = Exchange(asset, timeframe)
    #         dbm = DatabaseManager(asset, timeframe)
    #
    #         f = Features(dbm.get_dataframe())
    #         X, y = f.run_features()
    #         mlt = MachLearnTools(X, y)
    #         X_train, X_test, y_train, y_test = mlt.timeseries_pipeline()
    #
    #         # Looks like NN needs a manager or something 
    #         layers = [[8, "relu"], [8, "relu"]]
    #         model = NeuralNetwork(X_train, y_train, "binary", epochs = 1000, lr=0.02, layers=layers)
    #         model.fit()
    #
    #         x_pred = mlt.latest_features()
    #         x_pred = np.resize(x_pred, (1, model.X.shape[1]))  # force shape match if tiny diff
    #
    #         pred_val = model.predict(x_pred)
    #         direction = "Buy" if pred_val > 0.5 else "Sell"
    #
    #         # Using clustering to find the risk we will choose aka strategy
    #         strat = Strategy(X)
    #         risk = strat.main()
    #         risk_list.append(risk)
    #         dir_list.append(direction)
    #
    #         # Hardcoding for time being
    #         entry: float = int(float(ex.get_ohlc()[-1][1]))
    #         entry_list.append(entry)
    #
    #         # Hard coded arbitrary stop for the time being 
    #         stop, target = 0, 0
    #         if direction == "Buy":
    #             stop: int = int(float(ex.get_ohlc()[-2][3]))
    #             target: int = (entry - stop) * 2 + entry
    #         else: 
    #             stop: int = int(float(ex.get_ohlc()[-2][2]))
    #             target: int = entry - (stop - entry) * 2
    #         stop_list.append(stop)
    #         target_list.append(target)
    #
    #         # print(ex.get_ohlc()[-1])
    #
    #         c = RiskCalculator()
    #         size, risk_percentage = c.main(entry, stop, risk)
    #         size_list.append(size)
    #
    #     # Printing info instead of automating trade currently
    #     print(asset)
    #     print("Time Frame\t", end="")
    #     for t in time_list:
    #         print(f"{t}\t", end="")
    #     print("\nRisk Level\t", end="")
    #     for r in risk_list:
    #         print(f"{r}\t", end="")
    #     print("\nDirection\t", end="")
    #     for d in dir_list:
    #         print(f"{d}\t", end="")
    #     print("\nEntry Level\t", end="")
    #     for e in entry_list:
    #         print(f"${e:,}\t", end="")
    #     print("\nStop Level\t", end="")
    #     for s in stop_list:
    #         print(f"${s:,}\t", end="")
    #     print("\nTarget pri\t", end="")
    #     for t in target_list:
    #         print(f"${t:,}\t", end="")
    #     print("\nSize of Pos\t", end="")
    #     for p in size_list:
    #         print(f"${p:,} ", end="")
    #     print("\n")
    #
    #
