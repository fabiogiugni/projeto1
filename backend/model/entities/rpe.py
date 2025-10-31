from data import Data

class RPE(Data):

    def __init__(self, departmentIDs: list[str] = None):
        self.__departmentIDs = departmentIDs if departmentIDs is not None else []
    
    def addObjective(self, objectiveID: str):
        self.__departmentIDs.append(objectiveID)

    def deleteObjective(self, objectiveID: str):
        self.__departmentIDs.delete(objectiveID)