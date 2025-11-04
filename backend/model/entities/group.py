from .entity import Entity
from typing import TYPE_CHECKING

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Group(Entity):

    def __init__(self, name: str, id: str = None, rpeIds: list[str] = None):
        super().__init__(id)
        self._name = name
        self._rpeIds = rpeIds if rpeIds is not None else []

    def addRPE(self, RPEID : str, db: 'Database'):
        self._rpeIds.append(RPEID)

    def deleteRPE(self, RPEID : str, db: 'Database'):
        self._rpeIds.remove(RPEID)

    @property
    def rpeIds(self):
        return self._rpeIds

    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    
    @rpeIds.setter
    def rpeIds(self, rpeIds : str):
        self._rpeIds = rpeIds