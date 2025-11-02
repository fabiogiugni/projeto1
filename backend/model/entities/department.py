from .group import Group
from typing import TYPE_CHECKING

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Department(Group):

    def __init__(self, name: str, directorID: str, companyID:str, id: str = None, rpeIds: list[str] = None, teamIds: list[str] = None):
        super().__init__(name, id, rpeIds)
        self.__teamIds = teamIds if teamIds is not None else []
        self.__directorID = directorID
        self.__companyID = companyID

    def addTeam(self, teamID : str, db: 'Database'):
        self.__teamIds.append(teamID)
        db.updateItem(self)
    
    def removeTeam(self, teamID : str, db: 'Database'):
        self.__teamIds.remove(teamID)
        db.updateItem(self)

    @property
    def teamIds(self):
        return self.__teamIds

    @property
    def directorID(self):
        return self.__directorID
    
    @property
    def companyID(self):
        return self.__companyID

    @directorID.setter
    def directorID(self, directorID : str, db: 'Database'):
        self.__directorID = directorID
        db.updateItem(self)
