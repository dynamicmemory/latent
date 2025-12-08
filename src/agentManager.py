from src.miniML.models.neuralNetwork import NeuralNetwork 
from src.miniML.machLearnTools import MachLearnTools
from src.features import Features 
import numpy as np


class Agent:
    def main(self, dbm):
        f = Features(dbm.get_data())
        X, y = f.run_features()
        mlt = MachLearnTools(X, y)
        X_train, X_test, y_train, y_test = mlt.timeseries_pipeline()

        layers = [[8, "relu"], [8, "relu"]]
        model = NeuralNetwork(X_train, y_train, "binary", epochs = 5000, lr=0.02, layers=layers)
        model.fit()
        
        x_pred = mlt.latest_features()
        
        # TODO: MOVE INTO WHEREEVER IM DOING THIS... MLT I THINK
        x_pred = np.resize(x_pred, (1, model.X.shape[1]))  # force shape match if tiny diff
        
        pred_val = model.predict(x_pred)
        print("Buy" if pred_val > 0.5 else "sell")
