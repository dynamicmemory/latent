# TODO: Rebuild everything in here into my own scikitlearn equiv
    # Pulling the data in
    # Data cleaning 
    # Feature engineering 
    # Normalizing and scaling 
    # Data splitting 
    # Shaping 
    # Single pipeline that always produces the same result.
# TODO: Change the df to self.df... this class is so broken atm
# TODO: REDO labels to classify more fine grained lvls with % changes away from 0
import pandas as pd 
import numpy as np
from src.paths import get_data_path
from src.machLearnTools import MachLearnTools 

class Features:
    def __init__(self, fname: str) -> None:
        self.fname: str = fname
        self.path = get_data_path(fname)
        self.features: list[str] = []
        self.df = None
        self.mlt = MachLearnTools()

    # KEEP
    def compute_features(self) -> pd.DataFrame:
        """
        Temp function building all features inside of till finished fully
        """
        # ------------ FEATURE RELATED CODE ------------------
        df: pd.DataFrame = pd.read_csv(self.path)

        # Probably wont drop time for tfs that could use it as metric
        df.drop(["utc", "time"], axis=1, inplace=True)
        df["diff"] = df["close"] - df["open"]

        df["label"] = self.mlt.create_binary_labels(df["diff"])
        self.features.append("label")

        self.simple_moving_average(df, 50)
        self.simple_moving_average(df, 100)
        self.simple_moving_average(df, 200)
        self.rsi(df)
        self.df = df
        return df


    # KEEP
    def select_features(self, df) -> pd.DataFrame:
        cols = self.features.copy()
        selected = df[cols].dropna()
        return selected 

    
    # MOVE 
    def to_numpy(self, df, window=60) -> tuple: 
        # Normalize each feature (z-score)
        features = df[self.features]
        X_norm = (features - features.mean()) / features.std()
        
        labels = df["label"].to_numpy(dtype=np.float32)
        # labels = df["label"]
        data = X_norm.to_numpy(dtype=np.float32)

        X, y = [], []
        for i in range(window, len(data)):
            X.append(data[i-window:i])
            y.append(labels[i])

        return np.array(X), np.array(y).reshape(-1, 1)

 
    # MOVE 
    def build_data(self) -> tuple:
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
   
        X_train, X_test, y_train, y_test = self.mlt.split_data(X, y)
        return X_train, X_test, y_train, y_test 


    # TODO: Move this or rebuild this, just for proof of concept for the minute 
    def latest_features(self, window: int=60) -> list:
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


    #============================= CALCULATE FEATURES =========================
    # KEEP
    def simple_moving_average(self, df: pd.DataFrame, period: int) -> None:
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


    # KEEP
    def rsi(self, df: pd.DataFrame) -> None:
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
