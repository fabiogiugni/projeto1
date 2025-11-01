from .data import Data
from datetime import datetime

class RPE(Data):

    def __init__(self, description: str, responsibleID: str, date :datetime, id:str = None, objectiveIds: list[str] = None):
        super().__init__(description, responsibleID, date, id)
        self.__objectiveIds = objectiveIds if objectiveIds is not None else []
    
    def addObjective(self, objectiveID: str):
        self.__objectiveIds.append(objectiveID)

    def deleteObjective(self, objectiveID: str):
        self.__objectiveIds.remove(objectiveID)