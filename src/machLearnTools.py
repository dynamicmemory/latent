# Load data *done in features class
# compute targets/labels
# compute features  *done in features class 
# clean 
# split data 
# scale 
# Encode 
# train *done in nn 
# eval 


import numpy as np
import pandas as pd
# Full pipeline wrapper
class MachLearnTools:
    def pipeline(self, X, y) -> None:
        self.clean_data()
        self.split_data(self, X, y)
        s = DynamicScaler()
        e = Encoder().encode()
        pass


    def create_n_labels(self, y: list) -> None:
        """
        Creates binary labels 
        returns 
        """
        classes: set = set()
        for row in y:
            classes.add(row)
        pass


    def create_binary_labels(self, y: pd.Series|pd.DataFrame|list|np.ndarray) -> list[int]:
        """
        Create a 1D array of labels for a series of positive and negative values
        Returns a 1D array with 1 for positive and 0 for negative
        """
        y = np.asarray(y)
        return (y > 0).astype(int).tolist()


    def clean_data(self) -> None:
        pass 


    def split_data(self, X, y, t_size=0.2, seed=None, shuffle=False) -> tuple:
        """
        My trim down version of scikitlearns test_train_split. Splits the given 
        data into 4 outputs, the X train, X test, y train and y test set in that 
        order.
        Params: 
        X: Dataframe - Consisting of input features.
        y: 1d array - Array containing labels for the features.
        t_size: float - Percentage of the data put aside for testing.
        seed: int - Provide a random seed for consistance runs each time.
        shuffle: bool - Mix the features up so there is no order.
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


# Encode non number vals
class Encoder:
    def encode(self) -> None:
        pass

    def fit(self) -> None:
        pass

    def transform(self) -> None:
        pass

# TODO: Abstract is bounded and is outlier 
# TODO: Actually be serious and fix up / optimize all the ops, this is cool
# TODO: Change type from func calls to strings of names and update transform with 
#       switch to accomodate this change.
# Standard, MinMax or robust scaling
class DynamicScaler:
    def __init__(self) -> None: 
        self.scaler_types = [] 
        self.params: dict = {}


    def fit(self, X) -> None:
        for col in X.columns:
            if self._has_bounds(X[col], col):
                continue
            elif self._has_outliers(X[col], col):
                continue
            else:
                self._is_standard(X[col], col)


    def _has_bounds(self, X, name) -> bool:
        fmin: float = X.min()
        fmax: float = X.max()
        if fmin >= 0 and fmax <= 1e3:# TODO: Determine better range
            self.params[name] = {"type": self.min_max, "min": fmin, "max": fmax}
            return True
        return False

        
    def _has_outliers(self, X, name) -> bool:
        temp: dict = {"type": self.robust}
        q1: float = np.percentile(X, 25)
        q3: float = np.percentile(X, 75)
        iqr: float = q3 - q1

        one = (X < q1-3 * iqr).any()
        two = (X > q3+3 * iqr).any()
        if one or two:
            temp["q1"] = q1
            temp["q3"] = q3
            temp["iqr"] = iqr
            temp["median"] = np.median(X)
            self.params[name] = temp
            return True 
        return False


    def _is_standard(self, X, name) -> None:
        self.params[name] = {"type": self.standard,
                             "mean": X.mean(),
                             "std" : X.std()
                             }


    def transform(self, X) -> None:
        transformed = X.copy()
        for col in X.columns:
            transformed[col] = self.params[col]["type"](col, X[col])
        return transformed


    def min_max(self, name, X):
        """
        Scales features that are bounded below and above
        """
        X_max = self.params[name]["max"]
        X_min = self.params[name]["min"]
        X = np.asarray(X, dtype=float)
        return (X - X_min) / (X_max - X_min)
        

    def standard(self, name, X):
        """
        Scales features that have negative and positive values
        """
        mu = self.params[name]["mean"]
        std = self.params[name]["std"]
        X = np.asarray(X, dtype=float)
        return (X - mu) / std 


    def robust(self, name, X):
        """
        Scales features that are bounded > 0 and have many outliers 
        """
        median = self.params[name]["median"]
        q1 = self.params[name]["q1"]
        q3 = self.params[name]["q3"]
        iqr = self.params[name]["iqr"]

        X = np.asarray(X, dtype=float)
        return (X-median)/iqr


# Metrics for testing how good the model is
class Evaluate:
    def accuracy(self) -> None:
        pass


    def precision(self) -> None:
        pass 


    def recall(self) -> None:
        pass


    def f1_score(self) -> None:
        pass


# Back burners 
# pca 
# text embedding

