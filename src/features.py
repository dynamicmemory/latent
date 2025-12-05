# TODO: Once built, change to recieve cleaned df from external source, no csvread
# TODO: We can now move from df to self.df within the class, when ready.
import pandas as pd 
import numpy as np

class Features:
    def __init__(self, df: pd.DataFrame) -> None:
        self.features: list[str] = []
        self.df: pd.DataFrame = df


    # ============================= UTILS ====================================
    # If this was cut out, this whole thing wouldnt work, either build this to 
    # be more dynamic or build it specifically to be able to be replaced if you 
    # want this class to work on a different set of columns
    def compute_features(self) -> tuple:
        """ 
        Pipeline for this class, one call runs all functions
        Temp function building all features inside of till finished fully
        WILL BE WHAT IS CALLED TO PRODUCE THE DF TO BE FED INTO MLTOOLS
        """
        df = self.df

        # Probably wont drop time for tfs that could use it as metric
        df.drop(["utc", "time"], axis=1, inplace=True)
        df["diff"] = df["close"] - df["open"]
        
        df["shifted_diff"] = df["close"].shift(-1) - df["open"].shift(-1)
        df["label"] = self.create_binary_labels(df["shifted_diff"])

        df.drop(["shifted_diff"], axis=1, inplace=True)

        self.simple_moving_average(df, 50)
        self.simple_moving_average(df, 100)
        self.simple_moving_average(df, 200)
        self.rsi(df)
        self.df = df
        
        # Clean out X and realign y, then return both, we are done here.
        X = self.clean(df)
        y = df.loc[X.index, "label"].copy()     # all rows that are in X now
        y = y.dropna()
        X = X.loc[y.index]

        return X, y 


    def clean(self, df: pd.DataFrame, label:str="label") -> pd.DataFrame:
        """ Cleans a df of inf values, removes all nans, keeps labels aligned
            for all columns in self.features.
        """
        # Copy the df so as to keep the original with all raw data for later
        df = df.copy()
        # Any infinite values become NaNs 
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        # Now drop all the NaNs from only the features we will use.
        df.dropna(subset=self.features, inplace=True)
        return df 


    # TODO: Create finer grained labels depending on % change magnitude
    def create_binary_labels(self, y) -> list[int]:
        """
        Create a 1D array of labels for a series of positive and negative values
        Returns a 1D array with 1 for positive and 0 for negative
        """
        y = np.asarray(y)
        return (y > 0).astype(int).tolist()


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

        self.features.append(sname)   # Add the new feature to the features list 


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
 
        # TODO: RUN THROUGH CLEAN AFTER
