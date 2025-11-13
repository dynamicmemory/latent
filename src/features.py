# TODO: Rebuild everything in here into my own scikitlearn equiv
# TODO: Change the df to self.df... this class is so broken atm
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, Input, Output, html, dcc
from src.paths import get_data_path

class Features:

    def __init__(self, fname: str):
        self.fname = fname
        self.path = get_data_path(fname)
        self.features = []
        self.df = None


    def compute_features(self):
        """
        Temp function building all features inside of till finished fully
        """
        # ------------ FEATURE RELATED CODE ------------------
        df = pd.read_csv(self.path)

        # Probably wont drop time for tfs that could use it as metric
        df.drop(["utc", "time"], axis=1, inplace=True)
        df["diff"] = df["close"] - df["open"]

        self.assign_labels(df)

        self.simple_moving_average(df, 50)
        self.simple_moving_average(df, 100)
        self.simple_moving_average(df, 200)
        self.rsi(df)
        self.df = df
        return df


    # TODO: Consider adding text labels too and thresholds for catagorical labesl 
    #       Big buy, buy, hold, sell, big sell.... etc more nuance.
    def assign_labels(self, df: pd.DataFrame) -> None:
        """
        Assigns the traning label to the dataframe by looking for the last 24 
        change to calculate whether or not it was a buy or sell.
        """
        # 1 for BUY 0 for SELL
        df["label"] = df["diff"].apply(lambda x: 1 if x > 0 else 0)
        self.features.append("label")


    def simple_moving_average(self, df: pd.DataFrame, period: int):
        """ 
        Calculates n period moving average 
        Params: 
        df = a pandas DataFrame
        period = moving average period 
        """
        sname: str = f"sma_{period}"
        df[sname] = df["close"].rolling(period).mean()

        # Backfill pre-period rows with first average value, this stops nans
        df[sname] = df[sname].fillna(df.loc[df[sname].first_valid_index(), sname])
        self.features.append(sname)   # Add the new feature to the features list 


    def rsi(self, df: pd.DataFrame):
        """
        Calculates the RSI for a given asset in a dataframe. 
        """
        df["gain"] = df["diff"].where(df["diff"] >= 0, 0) 
        df["loss"] = -df["diff"].where(df["diff"] <= 0, 0) 
        df["avgGain"] = df["gain"].rolling(14).mean()
        df["avgLoss"] = df["loss"].rolling(14).mean()
        df["rs"] = df["avgGain"] / df["avgLoss"]
        df["rsi"] = 100 - 100/(1+ df["rs"])
        df.drop(["gain", "loss", "avgGain", "avgLoss", "rs"], axis = 1, inplace=True)
        self.features.append("rsi")


    def select_features(self, df):
        cols = self.features.copy()
        selected = df[cols].dropna()
        return selected 

    
    def to_numpy(self, df, window=60): 
        # Normalize each feature (z-score)
        features = df[self.features]
        X_norm = (features - features.mean()) / features.std()
        
        labels = df["label"].to_numpy(dtype=np.float32)
        data = X_norm.to_numpy(dtype=np.float32)

        X, y = [], []
        for i in range(window, len(data)):
            X.append(data[i-window:i])
            y.append(labels[i])

        return np.array(X), np.array(y).reshape(-1, 1)

 
    def split_train_test(self, X, y, ratio=0.8):
        split_idx = int(len(X) * ratio)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        return X_train, X_test, y_train, y_test


    def build_data(self):
        # calc all the features 
        df = self.compute_features()
        # select the features (can get rid of this eventually)
        df = self.select_features(df)
        # reshape the data
        X, y = self.to_numpy(df)
        # split the data 

        # flatten the moving window so this works for a vanilla ann, change once 
        # I build out better framework
        X = X.reshape(X.shape[0], -1)  # (samples, window * features)

        X_train, X_test, y_train, y_test = self.split_train_test(X, y)
        return X_train, X_test, y_train, y_test 


    # TODO: Move this or rebuild this, just for proof of concept for the minute 
    def latest_features(self, window: int=60):
        """
        Used to predict the next move in the market
        """
        # Redoing everythin in this class for the last 60 candles to produce a 
        # value to feed into the nn to predict the next market move.
        df_live = self.df.copy()

        feature_cols = self.features.copy()
        if "label" in feature_cols:
            feature_cols.remove("label")

        df_live = df_live[feature_cols].dropna()

        x_norm = (df_live - df_live.mean()) / df_live.std()

        X_input = x_norm[-window:].to_numpy(dtype=np.float32).reshape(1, -1)
        return X_input

















    # MOVE ALL BELOW CODE BACK INTO COMPUTE FUNCTION IF YOU WANT TO SEE IT WORK
    # ---- Chart related functions ----
    def add_line(self, fig, df: pd.DataFrame) -> None:
        averages = ["sma_50", "sma_100", "sma_200"]
        colours = ["blue", "orange", "magenta"]
        for n, avg in enumerate(averages):
            fig.add_trace(go.Scatter(x=df["date"], y=df[avg], mode="lines",
                          line=dict(width=1.5, color=colours[n]), name= avg))

       # ---------- PLOT RELATED CODE ---------------------
        y_values = ["sma_50", "sma_100", "sma_200"]
        line_fig = px.line(df, x="date", y=y_values, title="Price over time")
        fig2 = px.line(df, x="date", y="rsi", title="Price over time")
        # print(df)

        # Creates candlestick chart for price
        fig = go.Figure(data=[go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
        )])
        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_yaxes(fixedrange=False)
        self.add_line(fig, df)
        

        # ---------- DASHBOARD RELATED CODE ---------------------
        y_values = ["sma_50", "sma_100", "sma_200"]
        # Dash app to visualize what I am doing to the data.
        app = Dash(__name__)
        app.layout = [ 
            html.H1("Title"),
            dcc.Graph(id="price-chart", figure=fig, style={"height": "800px"}),
            dcc.Graph(id="rsi", figure=fig2)
        ]
        # app.run(debug=True)

