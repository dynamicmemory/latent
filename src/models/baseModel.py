from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def train(self, X, y) -> None:
        pass


    @abstractmethod
    def predict(self, X) -> float:
        pass 


    @abstractmethod
    def save(self, path: str) -> None:
        pass 


    @abstractmethod
    def load(self, path: str) -> None:
        pass
