from .data import Data
from typing import TYPE_CHECKING, Any, Dict, List

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Objective(Data):

    def __init__(self, description: str, responsibleID: str,date: str, rpeID: str, id:str = None):
        super().__init__(description, responsibleID, date, id)
        self.__rpeID = rpeID
    
    @property
    def rpeID(self):
        return self.__rpeID

    @rpeID.setter
    def rpeID(self, rpeID: str):
        """Setter para o rpeID"""
        if not isinstance(rpeID, str):
            raise TypeError("O nome deve ser uma string.")
        self.__rpeID = rpeID    

    def getData(self, db: 'Database'):
        data = super().getData(db)

        kpi_ids = db.getKPIsByObjective(self.id)
        kr_ids = db.getKRsByObjective(self.id)

        data["kpis"] = [
            db.getKPIByID(kpi_id).getData(db)
            for kpi_id in kpi_ids
            if db.getKPIByID(kpi_id)
        ]

        data["krs"] = [
            db.getKRByID(kr_id).getData(db)
            for kr_id in kr_ids
            if db.getKRByID(kr_id)
        ]

        return data
