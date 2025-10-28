from database import Database
from objective import Objective
from abc import ABC, abstractmethod


class FormasInterface(ABC):
   
    @abstractmethod
    def createObjective(obj: Objective, rpeID: str, db: Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def createKPI(kpi: KPI, objectiveID: str, db: Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def createKR(kr: KR, objectiveID: str, db: Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def deleteData(data: Data,db : Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def collectIndicator(id: str, db : Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def getData(groupID: str, db : Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass