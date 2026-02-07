from abc import ABC, abstractmethod

class IMenu(ABC):

    @abstractmethod
    def run(self) -> None:
        """Run this menu"""
        pass 


