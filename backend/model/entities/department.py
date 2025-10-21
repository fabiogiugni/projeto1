from import Group

class Department(Group):
    def __init__(self, id : int, name : str):
        super(id, name)
        self.__teamIDs = []
        self.__directorID = None

    def addTeam(self, teamID : int):
        self.__teamIDs.append(teamID)

    @property
    def directorID(self):
        return self.__directorID

    @directorID.setter
    def directorID(self, directorId : int):
        self.__directorID = directorId
