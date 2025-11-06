from .group import Group
from typing import TYPE_CHECKING

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Company(Group):

    def __init__(self, name: str, cnpj: str, id: str = None, rpeIds: list[str] = None, departmentIds: list[str] = None, directorIds: list[str] = None):
        # Repassa id, name e rpeIds para o Group
        super().__init__(name,id, rpeIds)
        self.__cnpj = cnpj
        self.__departmentIds = departmentIds if departmentIds is not None else []
        self.__directorIds = directorIds if directorIds is not None else []

    def addDepartment(self, departmentID : str, db: 'Database'):
        self.__departmentIds.append(departmentID)

    def removeDepartment(self, departmentID : str, db: 'Database'):
        self.__departmentIds.remove(departmentID)

    def addRPE(self, RPEID : str, db: 'Database'):
        super().addRPE(RPEID,db)
        db.addRpeToCompany(self.id,RPEID)
    
    def deleteRPE(self, RPEID : str, db: 'Database'):
        super().addRPE(RPEID,db)
        db.deleteRpeFromCompany(self.id,RPEID)

    @property
    def directorIds(self):
        return self.__directorIds
    
    @directorIds.setter
    def directorIds(self, id : str):
        self.__directorIds = id

    @property
    def departmentIds(self):
        return self.__departmentIds
    
    @departmentIds.setter
    def departmentIds(self, ids : str):
        self.__departmentIds = ids

    @property
    def cnpj(self):
        return self.__cnpj