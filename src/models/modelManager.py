from __future__ import annotations
from src.models.lstm import LSTM
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.baseModel import BaseModel 

class ModelManager:
    def __init__(self) -> None:
        self.model: BaseModel = LSTM() 


    def select(self, model: str, **kwargs) -> None:
        models = {
                "lstm": LSTM,
                # "cnn": CNN,
        }
        self.model = models[model](**kwargs)


    def train(self, X_train, y_train) -> None:
        self.model.train(X_train, y_train)


    def predict(self, X_latest, X_train) -> float:
        return self.model.predict(X_latest, X_train)


    def save(self, path) -> None:
        self.model.save(path)


    def load(self, path) -> None: 
        self.model.load(path)

