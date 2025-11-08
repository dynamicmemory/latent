import numpy as np 
import pandas as pd

class NN:
    def __init__(self, epochs: int, lr: float, structure: dict, features: pd.DataFrame):
        self.epochs = epochs
        self.learn_rate = lr
        # regularization 
        self.structure = structure # dict of layers and neurons/ins/outs and activations
        self.features : pd.DataFrame = features


    def init_weights(self):
        pass 

    
    def forward_pass(self):
        pass 


    def cross_entropy_loss(self):
        """
        Loss function for classification 
        """
        pass 


    def mean_squared_error(self):
        """
        Loss function for regression
        """
        pass


    def backprop(self):
        pass


    def update_weights(self):
        pass


    def train(self):
        pass


    def relu(self):
        pass 


    def soft_max(self):
        pass


    # Evaluate? maybe not in this class, maybe? dunno yet.
