from .group import Group

class Team(Group):

    def __init__(self, name: str, managerID: str=None, departmentID: str=None, id: str = None, rpeIds: list[str] = None, employeeIds: list[str] = None):
        super().__init__(name, id, rpeIds)
        self.__employeeIDs = employeeIds if employeeIds is not None else []
        self.__managerID = managerID
        self.__departmentID = departmentID

    def addEmployee(self, employeeID : str):
        self.__employeeIDs.append(employeeID)

    def removeEmployee(self, employeeID : str):
        self.__employeeIDs.remove(employeeID)

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
    def managerID(self, managerID : str):
        self.__managerID = managerID
        
    