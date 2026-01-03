import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# Determines how wide or narrow we assign training labels from returns
QUANTILE = 0.25
# Minumum return needed to beat fees and slippage (not applied currently) due to 
# 0.1% for the 15m is huge, but tiny for a daily candle, dynamic adjusting needed
MIN_RETURN = 0.1

class Features: 
    def __init__(self, df: pd.DataFrame) -> None: 
        self.df = df 
        self.features = ["open", "high", "low", "close", "volume"]


    def run_features(self) -> tuple:
        features = self.features
        df = self.df.copy()
        # Calculate the return 
        df["returns"] = (df["close"].shift(-1) / df["close"] - 1) * 100

        # Filter for top quantile
        upper_qrt = df["returns"].quantile(1 - QUANTILE)
        lower_qrt = df["returns"].quantile(QUANTILE)

        # Assign the labels (important we adjust returns for min return value eventually)
        df["label"] = np.where(df["returns"] >= upper_qrt, 1, 
                        np.where(df["returns"] <= lower_qrt, 0, 2))

        # Calculate all features 
        self.simple_moving_average(df, 50)
        self.simple_moving_average(df, 100)
        self.simple_moving_average(df, 200)
        self.rsi(df)
        self.volatility(df)

        # Clean, reshape and align the features and label dfs.
        X = self.clean(df)
        y = df.loc[X.index, "label"]     # all rows that are in X now
        self.features = features         # Reset features for the next call
        return X, y 


    #================================UTILS=====================================
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
        df["volatility"] = log_returns.rolling(period).std() * 100

        # 0-33=low 34-66=normal 67-90=high 91-100=extremee
        df["volatility_pctile"] = df["volatility"].rank(pct=True)

        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift(1)).abs()
        low_close = (df["low"] - df["close"].shift(1)).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df["atr_14"] = tr.rolling(14).mean()

        self.features.append("volatility")
        self.features.append("volatility_pctile")
        self.features.append("atr_14")


    # def plot_print_labels(self, lower, upper) -> None:
    #     # Plot return distributions
    #     plt.figure()
    #     plt.hist(self.df["returns"], bins=100)
    #     plt.axvline(x=lower, color="black")
    #     plt.axvline(x=upper, color="black")
    #     plt.savefig("returns_hist.png")
    #
    #     # Explore the results
    #     print(self.df.tail(10))
    #     label_counts = self.df["label"].value_counts().sort_index()
    #     print(len(label_counts), label_counts)
    #     for l in label_counts:
    #         print(l / len(self.df["label"]))
