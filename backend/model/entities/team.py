from .group import Group
from typing import TYPE_CHECKING

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Team(Group):

    def __init__(self, name: str, managerID: str=None, departmentID: str=None, id: str = None, rpeIds: list[str] = None, employeeIds: list[str] = None):
        super().__init__(name, id, rpeIds)
        self.__employeeIds = employeeIds if employeeIds is not None else []
        self.__managerID = managerID
        self.__departmentID = departmentID

    def addEmployee(self, employeeID : str, db: 'Database'):
        if employeeID not in self.__employeeIds:
            self.__employeeIds.append(employeeID)
        db.updateItem(self)

    def removeEmployee(self, employeeID : str, db: 'Database'):
        self.__employeeIds.remove(employeeID)
        db.updateItem(self)
    
    def addRPE(self, RPEID : str, db: 'Database'):
        super().addRPE(RPEID,db)
        db.addRpeToTeam(self.id,RPEID)
    
    def deleteRPE(self, RPEID : str, db: 'Database'):
        super().addRPE(RPEID,db)
        db.deleteRpeFromTeam(self.id,RPEID)

    @property
    def employeeIds(self):
        return self.__employeeIds

    @property
    def managerID(self):
        return self.__managerID
    
    @property
    def departmentID(self):
        return self.__departmentID

    @managerID.setter
    def managerID(self, managerID : str):
        self.__managerID = managerID