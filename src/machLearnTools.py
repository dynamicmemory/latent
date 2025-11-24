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
# Full pipeline wrapper
class MachLearnTools:

    def pipeline(self, X, y) -> None:
        self.compute_labels()
        self.clean_data()
        self.split_data(self, X, y)
        s = Scaler().scale()
        e = Encoder().encode()
        pass


    def compute_labels(self) -> None:
        pass


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


# Standard or MinMax scale
class Scaler:

    def scale(self) -> None:
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

