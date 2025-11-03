from .data import Data

from typing import TYPE_CHECKING, Any, Dict

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class KPI(Data):

    def __init__(self, description: str, responsibleID: str, date: str, objectiveID: str, id: str = None, data: list[float] = None):
        super().__init__(description, responsibleID, date, id)
        self._objectiveID = objectiveID
        self._data = data if data is not None else []

    def addData(self, data: float, db: 'Database'):
        self._data.append(data)
        db.updateItem(self)

    def deleteData(self, data: float, db: 'Database'):
        self._data.remove(data)
        db.updateItem(self)

    def getLastData(self):
        if not self._data:
            return None
        return self._data[-1]
    
    @property
    def objectiveID(self):
        return self._objectiveID
    
    @objectiveID.setter
    def objectiveID(self, objectiveID: str):
        """Setter para o objectiveID"""
        if not isinstance(objectiveID, str):
            raise TypeError("O nome deve ser uma string.")
        self._objectiveID = objectiveID 
    
    @property
    def data(self):
        return self._data
    
    def getData(self, db: 'Database') -> Dict[str, Any]:
        """Retorna os dados deste KPI em formato de dicionário."""
        # 1. Pega o dicionário base (id, desc, etc.)
        data_dict = super().getData(db)
        
        # 2. Adiciona os campos específicos do KPI
        data_dict.update({
            "collectedData": self._data,
            "lastValue": self.getLastData()
        })
        return data_dict
