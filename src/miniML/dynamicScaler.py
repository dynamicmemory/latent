# A Dynamic Scaler build primarily for scaling trading data, usable as normal
import numpy as np
import pandas as pd

class DynamicScaler:
    def __init__(self, range_dict: dict={}, outliers: float= 3) -> None: 
        """
        Initializes a dynamic scaler. 
        :Params:
        range_dict - allows specific lower and upper range vals for minmax scaling. 
        Dict keys must match feature names from the df. Example: {"rsi": (0,100)} 
        outliers - is the number of stds to assign to the outliers threshold 
        for the robust scaler.
        """
        self.params: dict = {}
        self.range_dict: dict[str, tuple] = range_dict
        self.outliers: float = outliers


    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Convience method for fitting and transforming X training at once."""
        self.fit(X)
        return self.transform(X)


    def fit(self, X: pd.DataFrame) -> None:
        """
        Dynamically assigns which scaler will apply to which feature in X 
        Options: Minmax, Robust, Standard
        """
        for feat in X.columns:
            if self._has_bounds(X[feat], feat):
                continue
            elif self._has_outliers(X[feat], feat): 
                continue
            else:
                # Standard scaling applies to those who meet no criteria
                self.params[feat] = {"type": "standard",
                                     "mean": X[feat].mean(),
                                     "std" : X[feat].std()}


    def _has_bounds(self, X, name: str) -> bool:
        """
        Tests column vector for bounded like values, assigns vector to minmax.
        """
        fmin: float = X.min()
        fmax: float = X.max()
        if name in self.range_dict:
            lower = self.range_dict[name][0]
            upper = self.range_dict[name][1]
        else:
            lower = 0
            upper = 100

        if fmin >= lower and fmax <= upper: 
            self.params[name] = {"type": "minmax", 
                                 "min": fmin, 
                                 "max": fmax}
            return True
        return False

        
    def _has_outliers(self, X, name: str) -> bool:
        """
        Tests column vector for outliers in values, assigns vector to Robust.
        """
        q1: float = float(np.percentile(X, 25))
        q3: float = float(np.percentile(X, 75))
        deviation: float = self.outliers * (q3 - q1)
        lower = (X < q1 - deviation).any()
        upper = (X > q3 + deviation).any()

        if lower or upper:
            self.params[name] = {"type": "robust",
                                 "median": np.median(X), 
                                 "q1":q1, "q3":q3}
            return True 
        return False


    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """ Transforms all features in X according to their stored type from 
        'fit' and returns the scaled features as a Dataframe
        """
        t = X.copy()
        for f in X.columns:
            scaler = self.params[f]["type"]
            if scaler == "minmax":
                t[f] = self.min_max(X[f], f)
            elif scaler == "robust":
                t[f] = self.robust(X[f], f)
            else:
                 t[f] = self.standard(X[f], f)
        return t


    def min_max(self, X, name: str):
        """
        Scales features that are bounded below and above
        """
        X_max: float = self.params[name]["max"]
        X_min: float = self.params[name]["min"]
        X = np.asarray(X, dtype=float)

        denom = X_max - X_min 
        if denom == 0:
            return np.zeros_like(X)
        return (X - X_min) / denom
        

    def robust(self, X, name: str):
        """
        Scales features that are bounded > 0 and have many outliers 
        """
        median: float = self.params[name]["median"]
        q1: float = self.params[name]["q1"]
        q3: float = self.params[name]["q3"]

        denom: float = q3 - q1 
        if denom == 0:
            return np.ones_like(X)

        X = np.asarray(X, dtype=float)
        return (X - median)/denom


    def standard(self, X, name: str):
        """
        Scales features that have negative and positive values
        """
        std: float = self.params[name]["std"] 
        if std == 0:
            return np.zeros_like(X)

        X = np.asarray(X, dtype=float)
        return (X - self.params[name]["mean"]) / std 

