from abc import ABC, abstractmethod

class DataInterface(ABC):

    @abstractmethod
    def printHistory() -> None:
        pass