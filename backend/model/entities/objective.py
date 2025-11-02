from .data import Data
from datetime import datetime

class Objective(Data):

    def __init__(self, description: str, responsibleID: str, date: datetime, id:str = None, kpiIds: list[str] = None, krIds: list[str] = None):
        super().__init__(description, responsibleID, date, id)
        self.__kpiIds = kpiIds if kpiIds is not None else []
        self.__krIds = krIds if krIds is not None else []
    
    def addKpi(self, kpiID: str):
        self.__kpiIds.append(kpiID)

    def deleteKpi(self, kpiID: str):
        self.__kpiIds.remove(kpiID)

    def addKr(self, krID: str):
        self.__krIds.append(krID)

    def deleteKr(self, krID: str):
        self.__krIds.remove(krID)