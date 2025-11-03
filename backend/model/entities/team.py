from .group import Group
from typing import TYPE_CHECKING

# Usado para type hinting
if TYPE_CHECKING:
    from ..database.database import Database

class Team(Group):

    def __init__(self, name: str, managerID: str=None, departmentID: str=None, id: str = None, rpeIds: list[str] = None, employeeIds: list[str] = None):
        super().__init__(name, id, rpeIds)
        self.__employeeIDs = employeeIds if employeeIds is not None else []
        self.__managerID = managerID
        self.__departmentID = departmentID

    def addEmployee(self, employeeID : str, db: 'Database'):
        self.__employeeIDs.append(employeeID)
        db.updateItem(self)

    def removeEmployee(self, employeeID : str, db: 'Database'):
        self.__employeeIDs.remove(employeeID)
        db.updateItem(self)

    @property
    def employeeIDs(self):
        return self.__employeeIDs

    @property
    def managerID(self):
        return self.__managerID
    
    @property
    def departmentID(self):
        return self.__departmentID

    @managerID.setter
    def managerID(self, managerID : str, db: 'Database'):
        self.__managerID = managerID
        db.updateItem(self)