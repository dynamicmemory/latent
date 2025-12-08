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

        # Clean, reshape and align the features and label dfs.
        X = self.clean(df)
        y = df.loc[X.index, "label"].copy()     # all rows that are in X now
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


    def rsi(self, df: pd.DataFrame) -> None:
        """Calculates the RSI for a given asset in a dataframe."""
        diff = "difference"
        if diff not in self.features:
            e = f"'{diff}' is missing from self.features, cant calc rsi"
            raise KeyError(e)

        df["gain"] = df[diff].where(df[diff] >= 0, 0) 
        df["loss"] = -df[diff].where(df[diff] <= 0, 0) 
        df["avg_gain"] = df["gain"].rolling(14).mean()
        df["avg_loss"] = df["loss"].rolling(14).mean()
        df["rs"] = df["avg_gain"] / df["avg_loss"]
        df["rsi"] = 100 - 100/(1+ df["rs"])

        df.drop(["gain", "loss", "avg_gain", "avg_loss", "rs"], axis = 1, inplace=True)

        self.features.append("rsi")


    def volatility(self, df: pd.DataFrame, period: int) -> None:
        """Calculates the volitility for the given asset"""
        diff: str = "difference"
        if diff not in self.features:
            e = f"'{diff}' is missing from self.features, cant calc volitility"
            raise KeyError(e)
         
        log_returns = np.log(df[diff] / df[diff].shift(1))
        df["volatility"] = log_returns.rolling(period).std(ddof=1) 

        self.features.append("volatility")

