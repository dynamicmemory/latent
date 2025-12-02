# TODO: Move this to the miniML dir and start splitting up the different classes
import numpy as np
import pandas as pd

# Full pipeline wrapper
class MachLearnTools:
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
        self.dynamic_scaler = DynamicScaler()
        self.X = X 
        self.y = y


    def pipeline(self) -> tuple:
        # self.clean_data()
        # self.split_data(self, X, y)
        # s = DynamicScaler()
        # e = Encoder().encode()
        return 1,2,3,4

    # TODO: Will be used to ensure data is clean during/post prepping for model
    def clean_data(self) -> None:
        pass 


    def split_data(self, X, y, t_size=0.2, seed=None, shuffle=False) -> tuple:
        """
        Spits data into 4 outputs, the X train, X test, y train and y test set 
        in that order.
        :Params: 
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


    # This is probably not need, just run clean data on self.features 
    # def select_features(self, df) -> pd.DataFrame:
    #     cols = self.features.copy()
    #     selected = df[cols].dropna()
    #     return selected 

    
    # MOVE 
    def convert_to_numpy(self, window=60) -> tuple: 
        # Scale the features 
        # features = df[self.features]
        features = self.X
        self.dynamic_scaler.fit(features)
        X_norm = self.dynamic_scaler.transform(features)
        
        # labels = df["label"].to_numpy(dtype=np.float32)
        labels = self.y.to_numpy(dtype=np.float32)
        data = X_norm.to_numpy(dtype=np.float32)

        X, y = [], []
        for i in range(window, len(data)):
            X.append(data[i-window:i])
            y.append(labels[i])

        return np.array(X), np.array(y).reshape(-1, 1)

 
    # MOVE 
    def build_data(self) -> tuple:
        # calc all the features 
        # df = self.compute_features()
        # select the features (can get rid of this eventually)
        # df = self.select_features(df)
        # reshape the data
        X, y = self.convert_to_numpy()
        # split the data 

        # flatten the moving window so this works for a vanilla ann, change once 
        # I build out better framework
        X = X.reshape(X.shape[0], -1)  # (samples, window * features)
   
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        return X_train, X_test, y_train, y_test 


   # TODO: Move this or rebuild this, just for proof of concept for the minute 
    def latest_features(self, window: int=60) -> np.ndarray:
        """
        Used to predict the next move in the market
        """
        # Redoing everythin in this class for the last 60 candles to produce a 
        # value to feed into the nn to predict the next market move.
        # df_live: pd.DataFrame = self.df.copy()
        df_live: pd.DataFrame = self.X.copy()

        # feature_cols = self.features.copy()
        feature_cols = df_live.columns
        # if "label" in feature_cols:
        #     feature_cols.remove("label")

        df_live = df_live[feature_cols].dropna()

        x_norm = self.dynamic_scaler.transform(df_live)
        X_input = x_norm[-window:].to_numpy(dtype=np.float32).reshape(1, -1)
        return X_input


# Encode non number vals
class Encoder:
    def encode(self) -> None:
        pass

    def fit(self) -> None:
        pass

    def transform(self) -> None:
        pass



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

# A Dynamic Scaler build primarily for scaling trading data, usable as normal
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
        """
        Transforms all features in X according to their stored type from 'fit'
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

