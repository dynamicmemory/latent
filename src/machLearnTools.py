# TODO: Move this to the miniML dir and start splitting up the different classes

# TODO: TIME SERIES IS OPTIONAL SO THE PIPELINE FOR IT SHOULD BE TOO CHSNGE CLASS FOR THIS

import numpy as np
from numpy.random import shuffle
import pandas as pd
from src.miniML.dynamicScaler import DynamicScaler 

# Full pipeline wrapper
class MachLearnTools:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
        self.dynamic_scaler = DynamicScaler()
        self.X = X 
        self.y = y

    
    # TODO: Split this into different concerns and specialize each task
    def run_pipeline(self, window:int = 60) -> tuple:
        # Scale the features 
        features = self.X
        self.dynamic_scaler.fit(features)
        X_norm = self.dynamic_scaler.transform(features)
        
        # Convert to arrays
        labels = self.y.to_numpy(dtype=np.float32)
        data = X_norm.to_numpy(dtype=np.float32)

        # Creates the sliding window
        X, y = [], []
        for i in range(window, len(data)):
            X.append(data[i-window:i])
            y.append(labels[i])

        # Turns the lists into arrays
        X, y = np.array(X), np.array(y).reshape(-1, 1)

        # Flattens windows for dense NN
        X = X.reshape(X.shape[0], -1)  # (samples, window * features)
   
        # Test train split                 # Shuffle false cause time series, change pipeline, build different one for time series data and make default for standard nn stuff.
        X_train, X_test, y_train, y_test = self.split_data(X, y, shuffle=False)
        return X_train, X_test, y_train, y_test 


    # TODO: Will be used to ensure data is clean during/post prepping for model
    def clean_data(self) -> None:
        # ACTUALLY USE THIS TO CLEAN THE DATA, MAYBE SHAPE IT TOO I DONT KNOW
        pass 


    def split_data(self, X, y, t_size=0.2, seed=None, shuffle=True) -> tuple:
        """ 
        Spits data into X train/test, y train/test set in that order.
        X: Dataframe - Consisting of input features.
        y: 1d array - Array containing labels for the features.
        t_size: float - Percentage of the data put aside for testing.
        seed: int - Provide a random seed for consistance runs each time.
        shuffle: bool - shuffle the rows of the dataset 
        """
        rng = np.random.default_rng(seed)

        X = np.array(X) if not isinstance(X, np.ndarray) else X
        y = np.array(y) if not isinstance(y, np.ndarray) else y
        if len(X) != len(y): raise ValueError("X and y must have identical length")

        # get t_sizes, ensure atleast 1 size in each
        n_samples = len(X)
        test_size = int(n_samples * t_size)
        train_size = n_samples - test_size
        if test_size < 1 or test_size >= n_samples:
            raise ValueError("t_size produces invalid sizes must be 0 < t_size < 1")
 
        #Shuffle
        idx = np.arange(n_samples)
        if shuffle:
            rng.shuffle(idx)

        train_idx = idx[:train_size]
        test_idx = idx[train_size:]

        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
             
        return (X_train, X_test, y_train, y_test)

    
    # REWRITE 
    def latest_features(self, window: int=60) -> np.ndarray:
        """
        Used to predict the next move in the market
        """
        # Redoing everythin in this class for the last 60 candles to produce a 
        # value to feed into the nn to predict the next market move.
        df_live: pd.DataFrame = self.X.copy()

        feature_cols = df_live.columns

        df_live = df_live[feature_cols].dropna()

        x_norm = self.dynamic_scaler.transform(df_live)
        X_input = x_norm[-window:].to_numpy(dtype=np.float32).reshape(1, -1)
        return X_input
