from database import Database
from abc import ABC, abstractmethod


class FormasInterface(ABC):
   
    @abstractmethod
    def createObjective(name: str, kpiIDs: str, krIDs: str) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def createKPI(name: str, responsibleID: str) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def createKR(name: str, goal: str, responsibleID: str) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def deleteData(id: str,db : Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def collectIndicator(id: str, db : Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def getData(teamID: str, db : Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass