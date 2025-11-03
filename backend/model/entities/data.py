from .entity import Entity

from typing import TYPE_CHECKING, Any, Dict

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

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
    def description(self, description: str, db: 'Database'):
        """Setter para description"""
        if not isinstance(description, str):
            raise TypeError("O nome deve ser uma string.")
        self._description = description
        db.updateItem(self)

    @responsibleID.setter
    def responsibleID(self, responsibleID: str, db: 'Database'):
        """Setter para o responsibleID"""
        if not isinstance(responsibleID, str):
            raise TypeError("O nome deve ser uma string.")
        self._responsibleID = responsibleID
        db.updateItem(self)

    def getData(self, db: 'Database') -> Dict[str, Any]:
        """Implementação base do getData da interface."""
        return {
            "id": self.id,
            "type": self.__class__.__name__, # Útil para o frontend
            "description": self.description,
            "responsibleID": self.responsibleID,
            "date": self.date
        }