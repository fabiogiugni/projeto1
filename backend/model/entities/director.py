from .person import Person
from .rpe import RPE
from .objective import Objective
from .kr import KR
from .data import Data
from .kpi import KPI

class Director(Person):

    def __init__(self, responsibleIds: list[str], **kwargs):
        super().__init__(**kwargs)
        self.__responsibleIDs = responsibleIds
        self._role = "Director"

    def createItem(self, item, db): #User, team, department...
        db.addItem(item)
    
    def deleteItem(self, item, db): #User, team, department...
        db.deleteItemByObject(item)

    def getDepartment(self, db):
        return db.getDepartmentByID(self.departmentID)
    
    def changeTeamManager(self, teamID : str, personID: str, db ):
        db.changeTeamManager(teamID, personID)
    
    def changeDepartmentDirector(self, departmentID : str, personID: str, db ):
        db.changeDepartmentDirector(departmentID, personID)
    
    def createObjective(self, obj: Objective, rpeID: str, db):
        db.addItem(obj)
        db.addObjectiveToRpe(obj.id,rpeID)
    
    def createKPI(self, kpi: KPI, objectiveID: str, db):
        db.addItem(kpi)
        db.addKpiToObjective(objectiveID,kpi.id)

    def createKR(self, kr: KR, objectiveID: str, db):
        db.addItem(kr)
        db.addKpiToObjective(objectiveID,kr.id)
    
    def deleteData(self, data: Data,db ):
        db.deleteItemByObject(data)

    def collectIndicator(self, kpi: KPI, db ):
        db.updateItem(kpi)