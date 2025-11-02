from .entity import Entity
from datetime import datetime

class Data(Entity):
    
    def __init__(self, description: str, responsibleID: str, date: str, id:str = None):
        super().__init__(id)
        self._description = description
        self._responsibleID = responsibleID
        self._date = date
    
    @property
    def description(self):
        return self._description
    
    @property
    def responsibleID(self):
        return self._responsibleID
    
    @property
    def date(self):
        return self._date
    
    @description.setter
    def description(self, description: str):
        """Setter para description"""
        if not isinstance(description, str):
            raise TypeError("O nome deve ser uma string.")
        self._description = description

    @responsibleID.setter
    def responsibleID(self, responsibleID: str):
        """Setter para o responsibleID"""
        if not isinstance(responsibleID, str):
            raise TypeError("O nome deve ser uma string.")
        self._responsibleID = responsibleID