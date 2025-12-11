import pandas as pd 
import numpy as np

class Features:
    def __init__(self, df: pd.DataFrame) -> None:
        # Start the features list off with the ohlc + volume from the market
        self.features: list[str] = ["open", "close", "high", "low", "volume"]
        self.df: pd.DataFrame = df


    def run_features(self) -> tuple:
        df = self.df.copy() 

        # Calculate the shifted price closes for generating training labels
        self.shift_difference(df)
        df["label"] = self.create_binary_labels(df["shifted_diff"])
        # Drop the shifted_difference to not leak future info in training
        df = df.drop(["shifted_diff"], axis=1)
        
        # Calculate all features 
        self.difference(df)
        self.simple_moving_average(df, 50)
        self.simple_moving_average(df, 100)
        self.simple_moving_average(df, 200)
        self.rsi(df)
        self.volatility(df)
        print(df)

        # Clean, reshape and align the features and label dfs.
        X = self.clean(df)
        y = df.loc[X.index, "label"]     # all rows that are in X now
        return X, y 


    #================================UTILS=====================================
    def shift_difference(self, df: pd.DataFrame) -> None:
        """ For timeseries data, shifts the labels off by one as to not peak 
        at the current realtime data for training queues
        """
        df["shifted_diff"] = df["close"].shift(-1) - df["open"].shift(-1)
        df.dropna(subset=["shifted_diff"], inplace=True)


    # TODO: Create finer grained labels depending on % change magnitude
    def create_binary_labels(self, y) -> list[int]:
        """
        Create a 1D array of labels for a series of positive and negative values
        Returns a 1D array with 1 for positive and 0 for negative
        """
        y = np.asarray(y)
        return (y > 0).astype(int).tolist()


    def clean(self, df: pd.DataFrame, label:str="label") -> pd.DataFrame:
        """ Cleans a df of inf values, removes all nans, keeps labels aligned
            for all columns in self.features.
        """
        # Copy the df so as to keep the original with all raw data for later
        df = df.copy()

        # Strip the dataframe down to only the features we want to train on
        features: list= [col for col in df.columns if col in self.features]
        df = df.loc[:, features]

        # Any infinite values become NaNs 
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        # Now drop all the NaNs from only the features we will use.
        df.dropna(subset=self.features, inplace=True)
        return df 


    # ==========================FEATURE CALCULATIONS==========================
    # TODO: Add percent change
    def difference(self, df: pd.DataFrame) -> None:
        """ Calculates the intra-timeframe difference between 'open' and 'close'
        features in the DataFrame 
        """
        df["difference"] = df["close"] - df["open"]
        self.features.append("difference")


    def simple_moving_average(self, df: pd.DataFrame, period: int) -> None:
        """ 
        Calculates n period moving average 
        Params: 
        df = a pandas DataFrame
        period = moving average period 
        """
        sname: str = f"sma_{period}"
        df[sname] = df["close"].rolling(period).mean()

        self.features.append(sname)  


    def rsi(self, df: pd.DataFrame, period:int=14) -> None:
        """Calculates the RSI for a given asset in a dataframe."""
        delta = df["close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss
        df["rsi"] = 100 - 100 / (1 + rs)

        self.features.append("rsi")


    def volatility(self, df: pd.DataFrame, period:int=30) -> None:
        """Calculates the volitility for the given asset"""
         
        log_returns = np.log(df["close"] / df["close"].shift(1))
        df["volatility"] = log_returns.rolling(period).std()  * 100

        # z store for standard volatilty calcs
        df["volatility_z"] = (df["volatility"] - df["volatility"].rolling(30).mean()) / df["volatility"].rolling(30).std()

        conditions = [df["volatility_z"] < -1, df["volatility_z"].between(-1, 1),
                      df["volatility_z"].between(1, 2),
                      df["volatility_z"] > 2 
                      ]
        # I dont have an encoder built yet so i have to convert these to nums 
        choices = ["low", "normal", "high", "extreme"]
        choices = [1, 2, 3, 4]
        df["risk_regime"] = np.select(conditions, choices, default=2)

        # 0-33=low 34-66=normal 67-90=high 91-100=extremee
        df["volatility_pctile"] = df["volatility"].rank(pct=True)

        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift(1)).abs()
        low_close = (df["low"] - df["close"].shift(1)).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df["atr_14"] = tr.rolling(14).mean()


        self.features.append("volatility")
        self.features.append("volatility_z")
        self.features.append("risk_regime")
        self.features.append("volatility_pctile")
        self.features.append("atr_14")

