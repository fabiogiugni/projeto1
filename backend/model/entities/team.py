from group import Group

class Team(Group):
    def __init__(self, name: str, managerID: str, id: str = None, RPEIDs: list[str] = None, employeesIDs: list[str] = None):
        super().__init__(name, id, RPEIDs)
        self.__employeeIDs = employeesIDs if employeesIDs is not None else []
        self.__managerID = managerID

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

    @managerID.setter
    def managerID(self, managerID : str):
        self.__managerID = managerID
        
    