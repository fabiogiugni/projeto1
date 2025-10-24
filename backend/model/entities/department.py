from group import Group

class Department(Group):
    def __init__(self, id : str, name : str):
        super().__init__(id, name)
        self.__teamIDs = []
        self.__directorID = None

    def addTeam(self, teamID : str):
        self.__teamIDs.append(teamID)
    
    def removeTeam(self, teamID : str):
        self.__departmentIDs.remove(teamID)

    @property
    def teamIDs(self):
        return self.__teamIDs

    @property
    def directorID(self):
        return self.__directorID

    @directorID.setter
    def directorID(self, directorId : str):
        self.__directorID = directorId
