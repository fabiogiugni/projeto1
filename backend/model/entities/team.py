from group import Group

class Team(Group):
    def __init__(self, id : int, name : str):
        super(id, name)
        self.__employeeIDs = []
        self.__managerID = None

    def addEmployee(self, employeeID : int):
        self.__employeeIDs.append(employeeID)

    def removeEmployee(self, employeeID : int):
        self.__departmentIDs.remove(employeeID)

    @property
    def managerID(self):
        return self.__managerID

    @managerID.setter
    def managerID(self, directorId : int):
        self.__managerID = managerId
        
        
    