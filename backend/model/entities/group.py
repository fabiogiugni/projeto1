from .entity import Entity
from typing import TYPE_CHECKING

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Group(Entity):

    def __init__(self, name: str, id: str = None, RPEIDs: list[str] = None):
        super().__init__(id)
        self._name = name
        self._RPEIDs = RPEIDs if RPEIDs is not None else []

    def addRPE(self, RPEID : str, db: 'Database'):
        self._RPEIDs.append(RPEID)
        db.updateItem(self)

    def deleteRPE(self, RPEID : str, db: 'Database'):
        self._RPEIDs.remove(RPEID)
        db.updateItem(self)

    @property
    def RPEIDs(self):
        return self._RPEIDs

    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id