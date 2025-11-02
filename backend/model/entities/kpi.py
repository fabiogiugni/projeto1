from .data import Data
from datetime import datetime

class KPI(Data):

    def __init__(self, description: str, responsibleID: str, date: str, id: str = None, data: list[float] = None):
        super().__init__(description, responsibleID, date, id)
        self._data = data if data is not None else []

    def addData(self, data: float):
        self._data.append(data)

    def deleteData(self, data: float):
        self._data.remove(data)

    def getLastData(self):
        if not self._data:
            return None
        return self._data[-1]
