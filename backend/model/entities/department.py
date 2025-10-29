from group import Group

class Department(Group):
    def __init__(self, name: str, directorID: str, id: str = None, RPEIDs: list[str] = None, teamIDs: list[str] = None):
        super().__init__(name, id, RPEIDs)
        self.__teamIDs = teamIDs if RPEIDs is not None else []
        self.__directorID = directorID

    def addTeam(self, teamID : str):
        self.__teamIDs.append(teamID)
    
    def removeTeam(self, teamID : str):
        self.__teamIDs.remove(teamID)

    @property
    def teamIDs(self):
        return self.__teamIDs

    @property
    def directorID(self):
        return self.__directorID

    @directorID.setter
    def directorID(self, directorID : str):
        self.__directorID = directorID
