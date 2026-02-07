from __future__ import annotations
from src.models.lstm import LSTM
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.baseModel import BaseModel 

class ModelManager:
    def __init__(self) -> None:
        self.model: BaseModel | None = None
        pass


    def select(self, model: str, **kwargs) -> None:
        models = {
                "lstm": LSTM,
                # "cnn": CNN,
                # "" : ,
        }
        self.model = models[model](**kwargs)


    def train(self, X, y) -> None:
        if self.model is not None:
            self.model.train(X, y)
        return 


    def predict(self, X, x) -> None:
        if self.model is not None:
            self.model.predict(X, x)
        return 


    def save(self, path) -> None:
        if self.model is not None:
            self.model.save(path)
        return 


    def load(self, path) -> None: 
        if self.model is not None:
            self.model.load(path)
        return  
