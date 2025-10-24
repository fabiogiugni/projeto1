from group import Group

class Team(Group):
    def __init__(self, id : str, name : str):
        super().__init__(id, name)
        self.__employeeIDs = []
        self.__managerID = None

    def addEmployee(self, employeeID : str):
        self.__employeeIDs.append(employeeID)

    def removeEmployee(self, employeeID : str):
        self.__departmentIDs.remove(employeeID)

    @property
    def employeeIDs(self):
        return self.__employeeIDs

    @property
    def managerID(self):
        return self.__managerID

    @managerID.setter
    def managerID(self, managerID : str):
        self.__managerID = managerID
        
        
    