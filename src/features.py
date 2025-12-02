# TODO: Once built, change to recieve cleaned df from external source, no csvread
import pandas as pd 
import numpy as np
from src.miniML import dynamicScaler
from src.paths import get_data_path
from src.machLearnTools import MachLearnTools, DynamicScaler 

class Features:
    def __init__(self, fname: str) -> None:
        self.fname: str = fname
        self.path = get_data_path(fname)
        self.features: list[str] = []
        self.df: pd.DataFrame 


    #============================= CALCULATE FEATURES =========================
    # Pipeline for this class, one call runs all functions
    def compute_features(self) -> tuple:
        """
        Temp function building all features inside of till finished fully
        
        WILL BE WHAT IS CALLED TO PRODUCE THE DF TO BE FED INTO MLTOOLS
        """
        # ------------ FEATURE RELATED CODE ------------------
        df: pd.DataFrame = pd.read_csv(self.path)

        # Probably wont drop time for tfs that could use it as metric
        df.drop(["utc", "time"], axis=1, inplace=True)
        df["diff"] = df["close"] - df["open"]
        
        df["label"] = self.create_binary_labels(df["diff"])
        # self.features.append("label")

        self.simple_moving_average(df, 50)
        self.simple_moving_average(df, 100)
        self.simple_moving_average(df, 200)
        self.rsi(df)
        self.df = df
        
        feature_cols = [col for col in self.features if col != "label"]
        X = df.loc[:, feature_cols].dropna().copy()   # only drop the nas here
        y = df.loc[X.index, "label"].copy()               # all rows that are in X now
        return X, y 


    # TODO: this needs to intelligently look for problems in the df after each 
    #       feature has been generated, and dynamically deal with each problem.
    def clean(self, df) -> pd.DataFrame:
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        pass


    # TODO: Create finer grained labels depending on % change magnitude
    def create_binary_labels(self, y) -> list[int]:
        """
        Create a 1D array of labels for a series of positive and negative values
        Returns a 1D array with 1 for positive and 0 for negative
        """
        y = np.asarray(y)
        return (y > 0).astype(int).tolist()


    def simple_moving_average(self, df: pd.DataFrame, period: int) -> None:
        """ 
        Calculates n period moving average 
        Params: 
        df = a pandas DataFrame
        period = moving average period 
        """
        sname: str = f"sma_{period}"
        df[sname] = df["close"].rolling(period).mean()

        # TODO: Replace with self.clean()
        # Backfill pre-period rows with first average value, this stops nans
        df[sname] = df[sname].fillna(df.loc[df[sname].first_valid_index(), sname])

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



        # Database -> DataService -> Features -> MLTools -> NN 
