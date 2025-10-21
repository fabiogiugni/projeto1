from import Group

class Team(Group):
    def __init__(self, id : int, name : str):
        super(id, name)
        self.__employeeIDs = []
        self.__managerID = None

    def addTeam(self, employeeID : int):
        self.__employeeIDs.append(employeeID)

    @property
    def managerID(self):
        return self.__managerID

    @managerID.setter
    def managerIDrID(self, directorId : int):
        self.__managerID = managerId
        
    