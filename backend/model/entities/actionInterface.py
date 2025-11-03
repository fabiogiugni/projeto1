from ..database.database import Database
from .objective import Objective
from .kpi import KPI
from .kr import KR
from abc import ABC, abstractmethod


class ActionInterface(ABC):
   
    @abstractmethod
    def createObjective(self, obj: Objective, rpeID: str, db: Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def createKPI(self, kpi: KPI, objectiveID: str, db: Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def createKR(self, kr: KR, objectiveID: str, db: Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def deleteData(self, data, db : Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def collectIndicator(self, id: str, db : Database) -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def addResponsibleRpeId(self, rpdID: str, db: 'Database') -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass
    @abstractmethod
    def deleteResponsibleRpeId(self, rpdID: str, db: 'Database') -> None: #manager tem acesso a nivel de team e Director tem acesso a nivel de dpto
        pass