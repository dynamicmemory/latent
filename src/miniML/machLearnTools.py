import numpy as np
import pandas as pd
from src.miniML.dynamicScaler import DynamicScaler 

class MachLearnTools:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
        self.dynamic_scaler = DynamicScaler()
        self.X = X 
        self.y = y


    # TODO: Combined the different pipelines in an intelligent way
    def standard_pipeline(self) -> tuple:
        """ Standard machine learning pipeline for ANN type problems """
        X_scaled = self.dynamic_scaler.fit_transform(self.X)

        # Convert to arrays
        X = X_scaled.to_numpy(dtype=np.float32)
        y = self.y.to_numpy(dtype=np.float32)

        return self.split_data(X, y)


    # TODO: Split this into different concerns and specialize each task
    def timeseries_pipeline(self, window:int=10):
        """ Machine learning pipeline for Time series problems """
        X_scaled = self.dynamic_scaler.fit_transform(self.X)

        # Convert to arrays
        X = X_scaled.to_numpy(dtype=np.float32)
        y = self.y.to_numpy(dtype=np.float32)

        X_win, y_win = self.sliding_window(X, y, window) 
        # X_flat = self.flatten_window(X_win)      # Remove when finished cnn

        # return self.split_data(X_flat, y_win, shuffle=False)
        return self.split_data(X_win, y_win, shuffle=False)


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

        train_idx, test_idx = idx[:train_size], idx[train_size:]

        return X[train_idx], X[test_idx], y[train_idx], y[test_idx]         


    def sliding_window(self, X: np.ndarray, y: np.ndarray, window:int=10) -> tuple: 
        """ Creates a sliding window for timeseries data """
        X_out, y_out = [], []
        for i in range(window, len(X)):
            X_out.append(X[i-window:i])
            y_out.append(y[i])

        # Turns the lists into arrays
        return np.array(X_out), np.array(y_out).reshape(-1, 1)


    # TODO: DELETE ONCE CNN BUILT 
    def flatten_window(self, X: pd.DataFrame) -> pd.DataFrame:
        """ Temporary until I build a CNN for timeseries"""
        # Flattens windows for dense NN
        return X.reshape(X.shape[0], -1)  # (samples, window * features)
    

    def latest_features(self, window:int=10) -> np.ndarray:
        """
        Used to predict the next move in the market. (Does not belong in mlt)
        scales => gets last n rows => converts to array => flattens to 1 row
        """
        X_scaled = self.dynamic_scaler.transform(self.X)
        return X_scaled[-window:].to_numpy(dtype=np.float32).reshape(1, -1)

